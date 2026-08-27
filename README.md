# Healthcare Research MCP Server

A healthcare research system built around the **Model Context Protocol (MCP)** that provides structured access to biomedical research from **PubMed** and **ClinicalTrials.gov**.

The project exposes healthcare research capabilities as MCP tools, prompts, and resources, while also providing a lightweight web interface for direct human use.

---

## Overview

Healthcare research often requires searching multiple sources, comparing evidence, and preserving identifiers such as PMIDs and NCT IDs.

This project provides a single research interface that can:

- Search PubMed for biomedical research articles
- Retrieve detailed PubMed article information
- Search ClinicalTrials.gov for clinical studies
- Combine evidence from multiple research sources
- Rank ClinicalTrials.gov results using lightweight relevance scoring
- Expose research capabilities through MCP
- Provide a structured research brief prompt
- Provide research methodology and safety guidelines as an MCP resource
- Provide a browser-based web interface
- Provide a standalone MCP demonstration client
- Validate user input and handle external API failures
- Preserve research identifiers for further review

The system is designed for **research assistance**, not individualized medical decision-making.

---

## Key Features

### PubMed

The server provides:

- `pubmed_search`
- `pubmed_get_article`

PubMed searches return structured article information such as:

- PMID
- Title
- Authors
- Journal
- Publication date

Article retrieval can provide additional information including available abstracts and DOI information.

---

### ClinicalTrials.gov

The server provides:

- `clinical_trials_search`

Clinical trial results include:

- NCT ID
- Study title
- Overall status
- Study type
- Conditions

The implementation performs a lightweight relevance ranking after retrieving candidate studies from ClinicalTrials.gov.

Query terms receive higher relevance when they occur in study titles, helping reduce unrelated results from broad searches.

---

### Multi-source Healthcare Research

The server provides:

- `healthcare_research`

This combines research retrieval from:

- PubMed
- ClinicalTrials.gov

The result is returned as a structured evidence package that can be consumed by an MCP client or the web application.

The workflow is deterministic rather than agentic. It follows predefined research steps instead of dynamically deciding which tools to use.

---

## MCP Capabilities

The project exposes three types of MCP capabilities.

### Tools

The MCP server currently exposes four tools:

| Tool | Purpose |
|---|---|
| `pubmed_search` | Search PubMed for biomedical research |
| `pubmed_get_article` | Retrieve detailed information for a PubMed article |
| `clinical_trials_search` | Search ClinicalTrials.gov |
| `healthcare_research` | Run a combined multi-source research workflow |

---

### Prompt

The server exposes:

```text
research_brief
```

The prompt generates a structured healthcare research brief containing:

1. Research question
2. Key findings
3. Relevant PubMed evidence
4. Relevant clinical trial evidence
5. Areas of agreement
6. Areas of uncertainty or conflicting evidence
7. Limitations
8. Sources requiring further review

The prompt explicitly instructs the consuming AI system to distinguish retrieved evidence from interpretation and avoid inventing unavailable findings.

---

### Resource

The server exposes:

```text
healthcare://research-guidelines
```

The resource contains guidelines covering:

- Evidence handling
- PMID and NCT preservation
- Distinguishing evidence from interpretation
- Research limitations
- Clinical trial status changes
- Independent review
- Medical safety

---

## Architecture

```text
                         User / AI Application
                                  |
                                  v
                         +----------------+
                         |   MCP Client   |
                         +----------------+
                                  |
                           MCP Protocol
                                  |
                                  v
                    +--------------------------+
                    |    Healthcare MCP Server  |
                    +--------------------------+
                       |        |        |
                       |        |        |
                    Tools     Prompt   Resource
                       |
                       v
              +-----------------------+
              | Research Workflow     |
              +-----------------------+
                   |             |
                   v             v
              +---------+   +----------------+
              | PubMed  |   | ClinicalTrials |
              +---------+   +----------------+
                   |             |
                   +------┬------+
                          |
                          v
                  Structured Evidence
                          |
                          v
                    MCP Client /
                    Web Interface
```

The web interface and MCP interface use the same underlying research functions.

---

## Why MCP?

The project could technically be implemented using ordinary Python functions and HTTP endpoints alone.

MCP adds a standardized interface between an AI application and the research capabilities.

Instead of building a separate custom integration for every AI client, the capabilities are exposed through MCP so compatible clients can discover and invoke:

- Tools
- Prompts
- Resources

Conceptually:

```text
AI Application
      |
      v
  MCP Client
      |
      v
  MCP Server
      |
      +---- Tools
      |
      +---- Prompts
      |
      +---- Resources
      |
      v
External Research APIs
```

This separation makes the research capabilities reusable by different MCP-compatible AI applications.

---

## Research Workflow

For a query such as:

```text
artificial intelligence ECG
```

the multi-source workflow performs the following:

```text
User Research Query
        |
        v
Input Validation
        |
        +----------------------+
        |                      |
        v                      v
     PubMed             ClinicalTrials.gov
        |                      |
        |                Candidate Studies
        |                      |
        |                Relevance Ranking
        |                      |
        +----------+-----------+
                   |
                   v
          Combined Evidence
                   |
                   v
          Structured JSON
```

The system does not claim that retrieved evidence proves causation unless the retrieved research supports such a conclusion.

---

## Project Structure

```text
healthcare-research-mcp/
│
├── demo.py
├── web_app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── server/
│   ├── __init__.py
│   ├── server.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── pubmed.py
│   │   ├── clinical_trials.py
│   │   └── research.py
│   │
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── research.py
│   │
│   ├── resources/
│   │   ├── __init__.py
│   │   └── guidelines.py
│   │
│   └── utils/
│       ├── errors.py
│       └── validation.py
│
└── tests/
    ├── test_client.py
    ├── test_mcp_server.py
    ├── test_research.py
    └── test_validation.py
```

---

## Technologies Used

- Python 3.11+
- Model Context Protocol
- FastMCP
- FastAPI
- Uvicorn
- Requests
- PubMed / NCBI APIs
- ClinicalTrials.gov API
- HTML
- CSS
- JavaScript
- Pytest

---

## Requirements

Python 3.11 or newer is recommended.

Install the dependencies with:

```bash
python -m pip install -r requirements.txt
```

The main dependencies are:

```text
mcp<2
requests
fastapi
uvicorn
```

---

## Setup

Clone the repository:

```bash
git clone https://github.com/Anubhab36/healthcare-research-mcp.git
cd healthcare-research-mcp
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

### Linux / ChromeOS

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Running the MCP Server

From the project root:

```bash
python -m server.server
```

The server communicates using MCP over standard input/output.

The server can then be connected to by an MCP-compatible client.

---

## Running the MCP Demo

A standalone demonstration client is included in:

```text
demo.py
```

Run:

```bash
python demo.py
```

The demo:

1. Starts the MCP server
2. Establishes an MCP connection
3. Discovers available tools
4. Discovers available prompts
5. Discovers available resources
6. Executes the multi-source healthcare research tool
7. Retrieves PubMed results
8. Retrieves ClinicalTrials.gov results
9. Displays sample evidence
10. Exits after completing the demonstration

Example:

```text
============================================================
 Healthcare Research MCP Server
============================================================

Connecting to MCP server...
✓ MCP connection established

[1] Available Tools
    ✓ pubmed_search
    ✓ pubmed_get_article
    ✓ clinical_trials_search
    ✓ healthcare_research

[2] Available Prompts
    ✓ research_brief

[3] Available Resources
    ✓ healthcare://research-guidelines

[4] Research Query
    artificial intelligence ECG

[5] Running healthcare research...
    ✓ PubMed: 3 results
    ✓ ClinicalTrials.gov: 3 results

[6] Sample PubMed Evidence
    PMID: 42646568
    Title: From Automated ECG Interpretation to Multimodal Cardiovascular Intelligence...

[7] Sample Clinical Trial
    NCT ID: NCT05942859
    Title: Applying Artificial Intelligence to the 12 Lead ECG for the Diagnosis of Pulmonary Hypertension...
    Status: ENROLLING_BY_INVITATION

============================================================
 MCP demonstration completed successfully
============================================================
```

---

## Running the Web Interface

The project also includes a lightweight browser-based interface.

Start the application with:

```bash
python -m uvicorn web_app:app --host 0.0.0.0 --port 8000
```

Then open:

```text
http://localhost:8000
```

The web interface provides a user-friendly way to submit research queries and view evidence without directly interacting with the MCP protocol.

The frontend communicates with the FastAPI backend, which uses the same healthcare research functionality exposed by the MCP server.

---

## Web Interface Architecture

```text
Browser
   |
   v
frontend/
   |
   v
FastAPI
(web_app.py)
   |
   v
Research Workflow
   |
   +--------+---------+
   |                  |
   v                  v
PubMed          ClinicalTrials.gov
   |                  |
   +--------+---------+
            |
            v
       Research Results
```

The frontend is intentionally lightweight. It acts as a demonstration and human-facing interface rather than replacing the MCP interface.

---

## Testing

The project includes automated tests for:

- Input validation
- Research workflow behavior
- MCP tool discovery
- MCP prompt discovery
- MCP resource discovery
- MCP client behavior

Run the complete test suite with:

```bash
python -m pytest -q
```

Current test status:

```text
9 passed
```

---

## Validation

Research queries and result limits are validated before external API requests are performed.

This helps prevent invalid requests from propagating into the research workflow.

---

## Error Handling

External research APIs can fail for reasons outside the application's control.

The project therefore handles:

- HTTP request failures
- Invalid JSON responses
- Missing research fields
- Source-specific failures
- Invalid user input

The research workflow can distinguish between successful source retrieval and unavailable source information rather than silently inventing results.

---

## Evidence Handling

The project follows several evidence-handling principles:

- Prefer retrieved source information over assumptions.
- Preserve PMID identifiers for PubMed evidence.
- Preserve NCT identifiers for clinical trial evidence.
- Clearly distinguish retrieved evidence from interpretation.
- Report when an abstract or other field is unavailable.
- Do not invent unavailable research findings.
- Do not automatically treat retrieved research as proof of causation.

Search results should not be assumed to represent the complete scientific literature.

Clinical trial status can also change over time.

---

## Medical Safety

This project is intended for **research assistance and evidence retrieval**.

It is not a substitute for:

- Professional medical judgment
- Clinical diagnosis
- Individualized treatment decisions
- Regulatory decision-making

Retrieved research should be independently reviewed before being used for clinical or regulatory decisions.

The system does not provide individualized medical advice.

---

## Limitations

### Literature Coverage

The system currently focuses on:

- PubMed
- ClinicalTrials.gov

It does not automatically search every biomedical database or scientific publisher.

### Search Completeness

Search results depend on the underlying APIs and query formulation.

A returned set of studies should not be interpreted as a complete systematic review.

### Relevance Ranking

ClinicalTrials.gov results receive lightweight local relevance ranking based primarily on query terms appearing in study titles and conditions.

This improves basic relevance but is not equivalent to a sophisticated semantic retrieval system.

### Abstract Availability

Some PubMed records may not contain an available abstract.

The application reports unavailable fields rather than generating missing research content.

### Clinical Trial Status

Clinical trial status may change after retrieval.

### No LLM Synthesis

The core research workflow retrieves and structures evidence. It does not require an LLM to generate or alter the underlying research data.

The `research_brief` MCP prompt can be supplied to an MCP-compatible AI application for structured synthesis.

---

## Security Considerations

The current project is designed primarily as a local research application.

For production deployment, additional security controls would be appropriate, including:

- Authentication
- Authorization
- Rate limiting
- Stronger input restrictions
- Secret management
- Request logging
- Monitoring
- Access control
- Secure remote MCP transport

The application should follow the principle of least privilege when connected to external systems.

---

## Future Improvements

Potential future enhancements include:

- Additional biomedical research sources
- More advanced semantic relevance ranking
- Research history and saved searches
- Citation export
- Advanced filtering
- LLM-assisted evidence synthesis
- Evidence-quality scoring
- Systematic-review workflows
- Authentication and authorization
- Production monitoring
- Automated CI/CD
- Public deployment

These are future extensions rather than required components of the current implementation.

---

## Project Status

The current implementation includes:

- MCP server
- Four MCP tools
- One MCP prompt
- One MCP resource
- PubMed integration
- ClinicalTrials.gov integration
- Multi-source research workflow
- Clinical trial relevance ranking
- Input validation
- Error handling
- Automated tests
- Standalone MCP demo client
- Lightweight web interface
- GitHub repository documentation

Current automated test result:

```text
9 passed
```

Public deployment is not currently included. The web interface is intended to run locally.

---

## Example Research Query

```text
artificial intelligence ECG
```

The system can retrieve biomedical literature and clinical trial information related to the query while preserving source identifiers for further investigation.

Example source identifiers:

```text
PMID: 42646568
NCT ID: NCT05942859
```

---

## Disclaimer

This project is an educational and research-oriented software system.

It provides structured access to biomedical research information and should not be used as a substitute for qualified medical, scientific, or regulatory expertise.

Always independently review the underlying research sources before making consequential decisions.

---

## License

This project is currently intended as an educational and portfolio project.

Add a formal open-source license if the repository is intended to be distributed or reused under specific licensing terms.
