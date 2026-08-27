const searchButton =
    document.getElementById("searchButton");

const researchQuery =
    document.getElementById("researchQuery");

const maxResults =
    document.getElementById("maxResults");

const errorMessage =
    document.getElementById("errorMessage");

const summarySection =
    document.getElementById("summarySection");

const resultsSection =
    document.getElementById("resultsSection");

const partialWarning =
    document.getElementById("partialWarning");

const partialWarningText =
    document.getElementById("partialWarningText");

const pubmedCount =
    document.getElementById("pubmedCount");

const trialCount =
    document.getElementById("trialCount");

const sourceStatus =
    document.getElementById("sourceStatus");

const sourceStatusLabel =
    document.getElementById("sourceStatusLabel");

const queryLabel =
    document.getElementById("queryLabel");

const pubmedResults =
    document.getElementById("pubmedResults");

const trialResults =
    document.getElementById("trialResults");

const statusDot =
    document.getElementById("statusDot");

const statusText =
    document.getElementById("statusText");


function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove("hidden");
}


function hideError() {
    errorMessage.textContent = "";
    errorMessage.classList.add("hidden");
}


async function checkApiHealth() {

    try {

        const response = await fetch(
            "/api/health"
        );

        if (!response.ok) {
            throw new Error();
        }

        statusDot.classList.add("online");
        statusText.textContent =
            "Research API Online";

    } catch {

        statusDot.classList.add("offline");
        statusText.textContent =
            "Research API Offline";
    }
}


function renderPubMed(results) {

    if (!results.length) {

        pubmedResults.innerHTML =
            '<div class="empty">No PubMed results found.</div>';

        return;
    }

    pubmedResults.innerHTML =
        results.map(article => {

            const pmid =
                article.pmid || "";

            const sourceLink = pmid
                ? `https://pubmed.ncbi.nlm.nih.gov/${encodeURIComponent(pmid)}/`
                : null;

            return `
                <article class="result-item">

                    ${
                        sourceLink
                        ? `
                            <a
                                class="identifier"
                                href="${sourceLink}"
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                PMID: ${pmid} ↗
                            </a>
                        `
                        : `
                            <span class="identifier">
                                PMID: N/A
                            </span>
                        `
                    }

                    <h4>
                        ${article.title || "Untitled article"}
                    </h4>

                    <p>
                        ${article.journal || "Journal unavailable"}
                    </p>

                    <p>
                        ${article.publication_date || "Date unavailable"}
                    </p>

                </article>
            `;

        }).join("");
}


function renderTrials(results) {

    if (!results.length) {

        trialResults.innerHTML =
            '<div class="empty">No clinical trials found.</div>';

        return;
    }

    trialResults.innerHTML =
        results.map(trial => {

            const nct =
                trial.nct_id || "";

            const sourceLink = nct
                ? `https://clinicaltrials.gov/study/${encodeURIComponent(nct)}`
                : null;

            return `
                <article class="result-item">

                    ${
                        sourceLink
                        ? `
                            <a
                                class="identifier"
                                href="${sourceLink}"
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                NCT: ${nct} ↗
                            </a>
                        `
                        : `
                            <span class="identifier">
                                NCT: N/A
                            </span>
                        `
                    }

                    <h4>
                        ${trial.title || "Untitled study"}
                    </h4>

                    <p>
                        Status:
                        ${trial.status || "Unavailable"}
                    </p>

                    <p>
                        Study type:
                        ${trial.study_type || "Unavailable"}
                    </p>

                    <p>
                        ${
                            (trial.conditions || [])
                                .join(", ")
                            || "Conditions unavailable"
                        }
                    </p>

                </article>
            `;

        }).join("");
}


function renderSourceErrors(errors) {

    if (!errors.length) {

        partialWarning.classList.add(
            "hidden"
        );

        sourceStatus.textContent = "2";
        sourceStatusLabel.textContent =
            "connected";

        return;
    }

    sourceStatus.textContent =
        String(2 - errors.length);

    sourceStatusLabel.textContent =
        "available";

    partialWarningText.textContent =
        errors
            .map(error =>
                `${error.source}: ${error.error}`
            )
            .join(" · ");

    partialWarning.classList.remove(
        "hidden"
    );
}


async function runResearch() {

    const query =
        researchQuery.value.trim();

    if (!query) {

        showError(
            "Please enter a research question."
        );

        return;
    }

    hideError();

    searchButton.disabled = true;

    searchButton.textContent =
        "Searching research sources...";

    try {

        const response = await fetch(
            "/api/research",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    query: query,

                    max_results:
                        Number(
                            maxResults.value
                        )
                })
            }
        );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Research request failed."
            );
        }

        const summary =
            data.summary || {};

        pubmedCount.textContent =
            summary.pubmed_result_count || 0;

        trialCount.textContent =
            summary.clinical_trial_result_count || 0;

        queryLabel.textContent =
            `Research question: ${query}`;

        renderPubMed(
            data.sources?.pubmed || []
        );

        renderTrials(
            data.sources?.clinical_trials || []
        );

        renderSourceErrors(
            data.source_errors || []
        );

        summarySection.classList.remove(
            "hidden"
        );

        resultsSection.classList.remove(
            "hidden"
        );

    } catch (error) {

        showError(
            error.message ||
            "Unable to complete research."
        );

    } finally {

        searchButton.disabled = false;

        searchButton.textContent =
            "Search Research";
    }
}


searchButton.addEventListener(
    "click",
    runResearch
);


researchQuery.addEventListener(
    "keydown",
    event => {

        if (
            event.key === "Enter" &&
            (event.ctrlKey || event.metaKey)
        ) {
            runResearch();
        }
    }
);


checkApiHealth();
