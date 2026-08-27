from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from server.tools.research import (
    run_healthcare_research,
)


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"


app = FastAPI(
    title="Healthcare Research MCP Web Interface",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)


class ResearchRequest(BaseModel):
    query: str
    max_results: int = 5


@app.get("/")
def index():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


@app.post("/api/research")
def research(request: ResearchRequest):

    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Research query cannot be empty.",
        )

    if request.max_results < 1:
        raise HTTPException(
            status_code=400,
            detail="max_results must be at least 1.",
        )

    if request.max_results > 20:
        raise HTTPException(
            status_code=400,
            detail="max_results cannot exceed 20.",
        )

    try:

        result = run_healthcare_research(
            query=query,
            max_results=request.max_results,
        )

        return result

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Research request failed: {exc}",
        )


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "Healthcare Research Web Interface",
    }
