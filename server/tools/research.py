from server.tools.pubmed import search_pubmed
from server.tools.clinical_trials import search_clinical_trials
from server.utils.validation import validate_query
from server.utils.errors import ResearchSourceError


def run_healthcare_research(
    query: str,
    max_results: int = 5,
) -> dict:
    """
    Search multiple healthcare research sources
    and return a combined evidence package.

    Individual source failures are recorded without
    discarding successful results from other sources.
    """

    validate_query(
        query,
        max_results,
    )

    pubmed_results = []
    clinical_trial_results = []

    source_errors = []

    try:
        pubmed_results = search_pubmed(
            query=query,
            max_results=max_results,
        )

    except ResearchSourceError as error:
        source_errors.append(
            {
                "source": error.source,
                "error": error.message,
            }
        )

    try:
        clinical_trial_results = (
            search_clinical_trials(
                query=query,
                max_results=max_results,
            )
        )

    except ResearchSourceError as error:
        source_errors.append(
            {
                "source": error.source,
                "error": error.message,
            }
        )

    return {
        "research_question": query,

        "sources": {
            "pubmed": pubmed_results,
            "clinical_trials": (
                clinical_trial_results
            ),
        },

        "summary": {
            "pubmed_result_count": len(
                pubmed_results
            ),
            "clinical_trial_result_count": len(
                clinical_trial_results
            ),
        },

        "source_errors": source_errors,

        "partial_results": bool(
            source_errors
        ),
    }
