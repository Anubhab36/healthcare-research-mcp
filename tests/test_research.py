from server.tools import research


def test_combined_research(monkeypatch):

    def fake_pubmed(query, max_results):
        return [
            {
                "pmid": "123456",
                "title": "Example PubMed Study",
            }
        ]

    def fake_trials(query, max_results):
        return [
            {
                "nct_id": "NCT12345678",
                "title": "Example Clinical Trial",
            }
        ]

    monkeypatch.setattr(
        research,
        "search_pubmed",
        fake_pubmed,
    )

    monkeypatch.setattr(
        research,
        "search_clinical_trials",
        fake_trials,
    )

    result = research.run_healthcare_research(
        "artificial intelligence ECG",
        max_results=5,
    )

    assert (
        result["research_question"]
        == "artificial intelligence ECG"
    )

    assert (
        result["summary"]["pubmed_result_count"]
        == 1
    )

    assert (
        result["summary"]["clinical_trial_result_count"]
        == 1
    )

    assert result["source_errors"] == []
    assert result["partial_results"] is False


def test_partial_source_failure(monkeypatch):

    def fake_pubmed(query, max_results):
        return [
            {
                "pmid": "123456",
                "title": "Example PubMed Study",
            }
        ]

    def fake_trials(query, max_results):
        raise research.ResearchSourceError(
            "ClinicalTrials.gov",
            "Temporary API failure",
        )

    monkeypatch.setattr(
        research,
        "search_pubmed",
        fake_pubmed,
    )

    monkeypatch.setattr(
        research,
        "search_clinical_trials",
        fake_trials,
    )

    result = research.run_healthcare_research(
        "artificial intelligence ECG",
        max_results=5,
    )

    assert (
        result["summary"]["pubmed_result_count"]
        == 1
    )

    assert (
        result["summary"]["clinical_trial_result_count"]
        == 0
    )

    assert result["partial_results"] is True

    assert len(
        result["source_errors"]
    ) == 1

    assert (
        result["source_errors"][0]["source"]
        == "ClinicalTrials.gov"
    )
