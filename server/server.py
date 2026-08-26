import json

from mcp.server.fastmcp import FastMCP

from server.tools.pubmed import (
    search_pubmed,
    get_pubmed_article,
)

from server.tools.clinical_trials import (
    search_clinical_trials,
)

from server.tools.research import (
    run_healthcare_research,
)

from server.prompts.research import (
    healthcare_research_brief,
)

from server.resources.guidelines import (
    RESEARCH_GUIDELINES,
)


mcp = FastMCP(
    "Healthcare Research Server"
)


# --------------------------------
# PubMed tools
# --------------------------------

@mcp.tool()
def pubmed_search(
    query: str,
    max_results: int = 5
) -> str:
    """
    Search PubMed for biomedical research articles.
    """

    results = search_pubmed(
        query=query,
        max_results=max_results,
    )

    return json.dumps(
        results,
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def pubmed_get_article(
    pmid: str,
) -> str:
    """
    Retrieve detailed information and abstract
    for a PubMed article using its PMID.
    """

    result = get_pubmed_article(
        pmid=pmid,
    )

    return json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
    )


# --------------------------------
# ClinicalTrials.gov tool
# --------------------------------

@mcp.tool()
def clinical_trials_search(
    query: str,
    max_results: int = 5
) -> str:
    """
    Search ClinicalTrials.gov for clinical studies.
    """

    results = search_clinical_trials(
        query=query,
        max_results=max_results,
    )

    return json.dumps(
        results,
        ensure_ascii=False,
        indent=2,
    )


# --------------------------------
# Multi-source research workflow
# --------------------------------

@mcp.tool()
def healthcare_research(
    query: str,
    max_results: int = 5
) -> str:
    """
    Search multiple healthcare research sources
    and return a combined evidence package.
    """

    result = run_healthcare_research(
        query=query,
        max_results=max_results,
    )

    return json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
    )


# --------------------------------
# Research prompt
# --------------------------------

@mcp.prompt()
def research_brief(
    research_question: str,
) -> str:
    """
    Generate a structured healthcare research
    brief prompt.
    """

    return healthcare_research_brief(
        research_question
    )


# --------------------------------
# Research resource
# --------------------------------

@mcp.resource(
    "healthcare://research-guidelines"
)
def research_guidelines() -> str:
    """
    Provide research methodology and safety
    guidelines for this MCP server.
    """

    return RESEARCH_GUIDELINES


if __name__ == "__main__":
    mcp.run()
