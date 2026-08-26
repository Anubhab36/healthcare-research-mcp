import requests

from server.utils.validation import validate_query
from server.utils.errors import ResearchSourceError


CLINICAL_TRIALS_API_URL = (
    "https://clinicaltrials.gov/api/v2/studies"
)


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

    response = requests.get(
        CLINICAL_TRIALS_API_URL,
        params={
            "query.term": query,
            "pageSize": max_results,
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

        conditions = protocol.get(
            "conditionsModule",
            {}
        )

        results.append(
            {
                "nct_id": identification.get(
                    "nctId",
                    ""
                ),
                "title": identification.get(
                    "briefTitle",
                    ""
                ),
                "status": status.get(
                    "overallStatus",
                    ""
                ),
                "study_type": design.get(
                    "studyType",
                    ""
                ),
                "conditions": conditions.get(
                    "conditions",
                    []
                ),
            }
        )

    return results
