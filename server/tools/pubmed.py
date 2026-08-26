import xml.etree.ElementTree as ET

import requests

from server.utils.validation import validate_query
from server.utils.errors import ResearchSourceError


NCBI_ESEARCH_URL = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
)

NCBI_ESUMMARY_URL = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
)

NCBI_EFETCH_URL = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
)


def search_pubmed(
    query: str,
    max_results: int = 5
) -> list[dict]:
    """
    Search PubMed and return basic metadata
    for matching research articles.
    """

    validate_query(
        query,
        max_results,
    )

    search_response = requests.get(
        NCBI_ESEARCH_URL,
        params={
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": max_results,
        },
        timeout=30,
    )

    try:
        search_response.raise_for_status()
        search_data = search_response.json()

    except requests.RequestException as exc:
        raise ResearchSourceError(
            "PubMed",
            f"Search request failed: {exc}",
        ) from exc

    except ValueError as exc:
        raise ResearchSourceError(
            "PubMed",
            "Search returned invalid JSON.",
        ) from exc

    ids = (
        search_data
        .get("esearchresult", {})
        .get("idlist", [])
    )

    if not ids:
        return []

    summary_response = requests.get(
        NCBI_ESUMMARY_URL,
        params={
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "json",
        },
        timeout=30,
    )

    try:
        summary_response.raise_for_status()
        summary_data = summary_response.json()

    except requests.RequestException as exc:
        raise ResearchSourceError(
            "PubMed",
            f"Summary request failed: {exc}",
        ) from exc

    except ValueError as exc:
        raise ResearchSourceError(
            "PubMed",
            "Summary request returned invalid JSON.",
        ) from exc

    results = []

    for pmid in ids:

        article = (
            summary_data
            .get("result", {})
            .get(pmid)
        )

        if not article:
            continue

        authors = [
            author.get("name")
            for author in article.get(
                "authors",
                []
            )
            if author.get("name")
        ]

        results.append(
            {
                "pmid": pmid,
                "title": article.get(
                    "title",
                    ""
                ),
                "authors": authors,
                "journal": article.get(
                    "fulljournalname",
                    ""
                ),
                "publication_date": article.get(
                    "pubdate",
                    ""
                ),
            }
        )

    return results


def get_pubmed_article(
    pmid: str
) -> dict:
    """
    Retrieve detailed PubMed article information
    using a PMID.
    """

    if not pmid.strip():
        raise ValueError(
            "PMID cannot be empty."
        )

    response = requests.get(
        NCBI_EFETCH_URL,
        params={
            "db": "pubmed",
            "id": pmid,
            "retmode": "xml",
        },
        timeout=30,
    )

    try:
        response.raise_for_status()

    except requests.RequestException as exc:
        raise ResearchSourceError(
            "PubMed",
            f"Article request failed: {exc}",
        ) from exc

    try:
        root = ET.fromstring(
            response.text
        )
    except ET.ParseError as exc:
        raise ValueError(
            "PubMed returned invalid XML."
        ) from exc

    article = root.find(
        ".//PubmedArticle"
    )

    if article is None:
        raise ValueError(
            f"No PubMed article found for PMID {pmid}."
        )

    title = extract_text(
        article.find(
            ".//ArticleTitle"
        )
    )

    journal = extract_text(
        article.find(
            ".//Journal/Title"
        )
    )

    authors = []

    for author in article.findall(
        ".//AuthorList/Author"
    ):
        last_name = extract_text(
            author.find("LastName")
        )

        initials = extract_text(
            author.find("Initials")
        )

        collective_name = extract_text(
            author.find("CollectiveName")
        )

        if collective_name:
            authors.append(
                collective_name
            )

        elif last_name:
            if initials:
                authors.append(
                    f"{last_name} {initials}"
                )
            else:
                authors.append(
                    last_name
                )

    abstract_sections = []

    for abstract in article.findall(
        ".//Abstract/AbstractText"
    ):
        text = extract_text(
            abstract
        )

        if not text:
            continue

        label = abstract.attrib.get(
            "Label"
        )

        if label:
            abstract_sections.append(
                f"{label}: {text}"
            )
        else:
            abstract_sections.append(
                text
            )

    abstract = "\n\n".join(
        abstract_sections
    )

    doi = ""

    for article_id in article.findall(
        ".//PubmedData/ArticleIdList/ArticleId"
    ):
        if article_id.attrib.get(
            "IdType"
        ) == "doi":
            doi = (
                article_id.text or ""
            ).strip()
            break

    publication_date = extract_publication_date(
        article
    )

    return {
        "pmid": pmid,
        "title": title,
        "authors": authors,
        "journal": journal,
        "publication_date": publication_date,
        "doi": doi,
        "abstract": abstract,
        "abstract_available": bool(abstract),
    }


def extract_text(
    element
) -> str:
    """
    Extract all text contained within an XML element,
    including text from nested elements.
    """

    if element is None:
        return ""

    return " ".join(
        "".join(
            element.itertext()
        ).split()
    )


def extract_publication_date(
    article
) -> str:
    """
    Extract the most useful publication date available
    from a PubMed article.
    """

    pub_date = article.find(
        ".//JournalIssue/PubDate"
    )

    if pub_date is None:
        return ""

    year = extract_text(
        pub_date.find("Year")
    )

    month = extract_text(
        pub_date.find("Month")
    )

    day = extract_text(
        pub_date.find("Day")
    )

    medline_date = extract_text(
        pub_date.find("MedlineDate")
    )

    if year:
        parts = [year]

        if month:
            parts.append(month)

        if day:
            parts.append(day)

        return " ".join(parts)

    return medline_date
