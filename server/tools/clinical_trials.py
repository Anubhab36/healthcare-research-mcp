import re

import requests

from server.utils.validation import validate_query
from server.utils.errors import ResearchSourceError


CLINICAL_TRIALS_API_URL = (
    "https://clinicaltrials.gov/api/v2/studies"
)


def _query_terms(query: str) -> list[str]:
    """
    Extract meaningful search terms from a query.
    """

    return [
        term.lower()
        for term in re.findall(r"[A-Za-z0-9]+", query)
        if len(term) > 2
    ]


def _relevance_score(
    query: str,
    title: str,
    conditions: list[str],
) -> int:
    """
    Calculate a lightweight relevance score based
    on query terms appearing in study title or conditions.
    """

    terms = _query_terms(query)

    searchable_text = " ".join(
        [title] + conditions
    ).lower()

    score = 0

    for term in terms:

        if term in title.lower():
            score += 3

        elif term in searchable_text:
            score += 1

    return score


def search_clinical_trials(
    query: str,
    max_results: int = 5
) -> list[dict]:
    """
    Search ClinicalTrials.gov for clinical studies.

    Returns basic study information including
    NCT ID, title, status, study type, and conditions.
    """

    validate_query(
        query,
        max_results,
    )

    # Retrieve a few additional records so that
    # relevance filtering has enough candidates.
    page_size = min(
        max_results * 3,
        20,
    )

    response = requests.get(
        CLINICAL_TRIALS_API_URL,
        params={
            "query.term": query,
            "pageSize": page_size,
            "format": "json",
        },
        timeout=30,
    )

    try:

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as exc:

        raise ResearchSourceError(
            "ClinicalTrials.gov",
            f"Search request failed: {exc}",
        ) from exc

    except ValueError as exc:

        raise ResearchSourceError(
            "ClinicalTrials.gov",
            "Search returned invalid JSON.",
        ) from exc

    studies = data.get(
        "studies",
        []
    )

    results = []

    for study in studies:

        protocol = study.get(
            "protocolSection",
            {}
        )

        identification = protocol.get(
            "identificationModule",
            {}
        )

        status = protocol.get(
            "statusModule",
            {}
        )

        design = protocol.get(
            "designModule",
            {}
        )

        conditions_module = protocol.get(
            "conditionsModule",
            {}
        )

        title = identification.get(
            "briefTitle",
            ""
        )

        conditions = conditions_module.get(
            "conditions",
            []
        )

        score = _relevance_score(
            query=query,
            title=title,
            conditions=conditions,
        )

        results.append(
            {
                "nct_id": identification.get(
                    "nctId",
                    ""
                ),
                "title": title,
                "status": status.get(
                    "overallStatus",
                    ""
                ),
                "study_type": design.get(
                    "studyType",
                    ""
                ),
                "conditions": conditions,
                "_relevance_score": score,
            }
        )

    results.sort(
        key=lambda item: item["_relevance_score"],
        reverse=True,
    )

    # Remove the internal scoring field before
    # returning results to the MCP client.
    for result in results:
        result.pop("_relevance_score", None)

    return results[:max_results]
