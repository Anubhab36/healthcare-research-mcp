# Healthcare Research MCP Server

A Model Context Protocol (MCP) server for structured healthcare research using real biomedical research sources.

The server provides MCP tools for searching PubMed and ClinicalTrials.gov, an MCP prompt for generating structured research briefs, and an MCP resource containing research and safety guidelines.

---

## 1. Project Overview

The Healthcare Research MCP Server provides a standardized interface between AI assistants and healthcare research sources.

Instead of requiring an AI application to implement separate integrations for every research database, the MCP server exposes healthcare research capabilities as reusable MCP tools.

The current implementation integrates:

- PubMed
- ClinicalTrials.gov

The server can search both sources for a research question and return a combined evidence package.

---

## 2. Problem Statement

Healthcare research often requires information from multiple sources.

A researcher may need to:

1. Search biomedical literature.
2. Retrieve individual research articles.
3. Search registered clinical trials.
4. Compare evidence across sources.
5. Keep track of identifiers such as PMID and NCT numbers.
6. Distinguish retrieved evidence from interpretation.

Without a standardized interface, each AI application would need to implement these integrations independently.

This project demonstrates how MCP can provide a reusable healthcare research interface.

---

## 3. Why MCP?

Model Context Protocol provides a standardized way for AI applications to interact with external tools, resources, and prompts.

This project demonstrates three major MCP primitives:

### Tools

Tools allow an MCP client or AI model to perform actions.

Implemented tools:

- `pubmed_search`
- `pubmed_get_article`
- `clinical_trials_search`
- `healthcare_research`

### Prompts

Prompts provide reusable instructions for a specific workflow.

Implemented prompt:

- `research_brief`

### Resources

Resources provide contextual information that an MCP client can retrieve.

Implemented resource:

- `healthcare://research-guidelines`

---

## 4. Architecture

                    MCP CLIENT
                        |
                        v
              Healthcare Research
                  MCP Server
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
      Tools           Prompts        Resources
        |               |               |
        |               |               |
        |        research_brief   research-guidelines
        |
   +----+---------------------+
   |                          |
   v                          v
 PubMed                ClinicalTrials.gov
   |                          |
   +------------+-------------+
                |
                v
        Combined Evidence
             Package

The server separates evidence retrieval from interpretation.

The MCP server retrieves and structures research information. An AI client can then use that evidence together with the research prompt to produce a structured research brief.

---

## 5. MCP Tools

### `pubmed_search`

Searches PubMed for biomedical research articles.

Example query:

artificial intelligence ECG

Returns:

- PMID
- Title
- Authors
- Journal
- Publication date

---

### `pubmed_get_article`

Retrieves detailed information for a PubMed article using its PMID.

Example:

PMID: 42642304

The response can include:

- PMID
- Title
- Journal
- Authors
- Publication date
- DOI
- Abstract when available

---

### `clinical_trials_search`

Searches ClinicalTrials.gov for clinical studies.

Returns structured information about matching studies, including identifiers and study information.

---

### `healthcare_research`

Performs a multi-source research search.

The workflow is:

Research Question
       |
       +------> PubMed
       |
       +------> ClinicalTrials.gov
       |
       v
Combined Evidence Package

The tool also reports source failures without discarding successful results from other sources.

---

## 6. MCP Prompt

### `research_brief`

The `research_brief` prompt provides a structured framework for synthesizing retrieved healthcare research.

It asks for:

1. Research question
2. Key findings
3. Relevant PubMed evidence
4. Relevant clinical trial evidence
5. Areas of agreement
6. Areas of uncertainty or conflicting evidence
7. Limitations
8. Sources requiring further review

The prompt also instructs the AI to:

- Avoid inventing findings.
- Distinguish evidence from interpretation.
- Avoid unsupported causal claims.
- Identify unavailable information.
- Preserve PMID and NCT identifiers.
- Avoid individualized medical advice.

---

## 7. MCP Resource

### `healthcare://research-guidelines`

Provides research methodology and safety guidance to an MCP client.

The resource covers:

- Evidence handling
- Source identifiers
- Research limitations
- Uncertainty
- Clinical safety boundaries
- The distinction between research information and professional medical judgment

---

## 8. Multi-Source Research Workflow

A typical workflow looks like:

User:
"What is the current evidence for AI-assisted ECG interpretation?"
                         |
                         v
                MCP Client / AI
                         |
                         v
              healthcare_research
                         |
              +----------+----------+
              |                     |
              v                     v
           PubMed          ClinicalTrials.gov
              |                     |
              +----------+----------+
                         |
                         v
                Evidence Package
                         |
                         v
                  research_brief
                         |
                         v
                Structured Research
                     Brief

This architecture keeps source retrieval separate from AI interpretation.

---

## 9. Validation

Search inputs are validated before external requests are made.

Current validation includes:

- Query must be a string.
- Query cannot be empty.
- `max_results` must be an integer.
- `max_results` must be at least `1`.
- `max_results` cannot exceed `20`.

This prevents invalid requests from unnecessarily reaching external APIs.

---

## 10. Error Handling

External research APIs can temporarily fail or return unexpected responses.

The server uses controlled `ResearchSourceError` exceptions for external-source failures.

For multi-source research, a failure in one source does not automatically discard results from another source.

For example:

PubMed              -> SUCCESS
ClinicalTrials.gov  -> ERROR
                       |
                       v
                Partial Results
                + Source Error

This allows the client to distinguish between:

- Successful evidence retrieval.
- Partial retrieval.
- Source failures.

---

## 11. Testing

The project includes automated tests for:

- Input validation.
- Combined research workflow.
- Partial source failures.
- MCP tool discovery.
- MCP prompt discovery.
- MCP resource discovery.
- MCP resource retrieval.

Run the complete test suite:

python -m pytest -q

The project uses both unit-level tests and MCP integration tests.

---

## 12. Project Structure

healthcare-research-mcp/
|
├── server/
│   ├── __init__.py
│   ├── server.py
│   |
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── pubmed.py
│   │   ├── clinical_trials.py
│   │   └── research.py
│   |
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── research.py
│   |
│   ├── resources/
│   │   ├── __init__.py
│   │   └── guidelines.py
│   |
│   └── utils/
│       ├── errors.py
│       └── validation.py
|
├── tests/
│   ├── test_client.py
│   ├── test_mcp_server.py
│   ├── test_research.py
│   └── test_validation.py
|
├── .gitignore
├── requirements.txt
└── README.md

---

## 13. Installation

Clone the repository:

git clone https://github.com/Anubhab36/healthcare-research-mcp.git
cd healthcare-research-mcp

Create a virtual environment:

python3 -m venv venv

Activate it:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Install testing dependencies if required:

pip install pytest

---

## 14. Running the MCP Server

The server communicates through MCP stdio transport.

Run:

python -m server.server

The server is intended to be launched by an MCP client rather than accessed through a normal browser.

---

## 15. Running the MCP Test Client

The repository includes a test client that starts the MCP server and communicates with it over stdio.

Run:

python tests/test_client.py

The client demonstrates:

- MCP initialization.
- Tool discovery.
- Prompt discovery.
- Resource discovery.
- Resource retrieval.
- Healthcare research tool invocation.

---

## 16. Example Research Queries

Example:

artificial intelligence ECG

Other example queries include:

AI assisted medical imaging

machine learning cardiac diagnosis

artificial intelligence radiology

deep learning ECG analysis

machine learning clinical decision support

These queries can be used with the multi-source research workflow.

---

## 17. Healthcare Safety Considerations

This project is intended for healthcare research and information retrieval.

It is not intended to:

- Diagnose patients.
- Recommend individualized treatment.
- Replace medical professionals.
- Make autonomous clinical decisions.

Retrieved research should be independently reviewed before being used for clinical, regulatory, or other high-impact decisions.

Search results may be incomplete, and clinical trial information can change over time.

---

## 18. Design Principles

The project follows several design principles.

### Evidence before interpretation

The server retrieves source information before any AI synthesis occurs.

### Source traceability

Research identifiers such as PMID and NCT identifiers are preserved where available.

### Separation of responsibilities

The MCP server handles:

Data retrieval
Validation
Structuring
Source error handling

The consuming AI application can handle:

Interpretation
Comparison
Summarization
Research synthesis

### Graceful degradation

Failure of one research source should not automatically eliminate successful results from another source.

---

## 19. Technologies Used

- Python
- Model Context Protocol (MCP)
- FastMCP
- PubMed / NCBI
- ClinicalTrials.gov API
- pytest
- JSON
- stdio transport

---

## 20. Future Improvements

Potential future improvements include:

- Additional biomedical databases.
- Cross-source deduplication.
- Citation ranking.
- Date and publication filters.
- Study-type filtering.
- Evidence quality scoring.
- Full-text article retrieval where available.
- More advanced research synthesis.
- Persistent research sessions.
- MCP client integrations.
- Additional automated integration tests.

---

## 21. Project Goal

The primary goal of this project is to demonstrate how Model Context Protocol can be used to build a reusable AI interface for healthcare research.

Rather than building a single-purpose healthcare chatbot, the project provides standardized MCP capabilities that an AI client can discover and use as needed.

The result is a modular healthcare research infrastructure that separates:

Research Sources
       |
       v
MCP Tools
       |
       v
Structured Evidence
       |
       v
AI Interpretation

---

## License

This project is intended for educational and research purposes.
