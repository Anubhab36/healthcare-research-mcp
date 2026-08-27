import asyncio
import json
import logging
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


logging.disable(logging.INFO)


ROOT_DIR = Path(__file__).resolve().parent
SERVER_PATH = ROOT_DIR / "server" / "server.py"


async def main():
    print("=" * 60)
    print(" Healthcare Research MCP Server")
    print("=" * 60)

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "server.server"],
        cwd=str(ROOT_DIR),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            print("\nConnecting to MCP server...")
            await session.initialize()
            print("✓ MCP connection established")

            # ----------------------------------------
            # Tool discovery
            # ----------------------------------------

            print("\n[1] Available Tools")

            tools_result = await session.list_tools()

            for tool in tools_result.tools:
                print(f"    ✓ {tool.name}")

            # ----------------------------------------
            # Prompt discovery
            # ----------------------------------------

            print("\n[2] Available Prompts")

            prompts_result = await session.list_prompts()

            for prompt in prompts_result.prompts:
                print(f"    ✓ {prompt.name}")

            # ----------------------------------------
            # Resource discovery
            # ----------------------------------------

            print("\n[3] Available Resources")

            resources_result = await session.list_resources()

            for resource in resources_result.resources:
                print(f"    ✓ {resource.uri}")

            # ----------------------------------------
            # Research query
            # ----------------------------------------

            query = "artificial intelligence ECG"

            print("\n[4] Research Query")
            print(f"    {query}")

            # ----------------------------------------
            # Multi-source research
            # ----------------------------------------

            print("\n[5] Running healthcare research...")

            result = await session.call_tool(
                "healthcare_research",
                {
                    "query": query,
                    "max_results": 3,
                },
            )

            raw_text = ""

            for content in result.content:
                if hasattr(content, "text"):
                    raw_text += content.text

            research_data = json.loads(raw_text)

            sources = research_data.get(
                "sources",
                {}
            )

            pubmed_results = sources.get(
                "pubmed",
                []
            )

            trial_results = sources.get(
                "clinical_trials",
                []
            )

            source_errors = research_data.get(
                "source_errors",
                []
            )

            print(
                f"    ✓ PubMed: "
                f"{len(pubmed_results)} results"
            )

            print(
                f"    ✓ ClinicalTrials.gov: "
                f"{len(trial_results)} results"
            )

            if source_errors:
                print("\n    Source warnings:")

                for error in source_errors:
                    print(
                        f"    ! {error}"
                    )

            # ----------------------------------------
            # Display sample evidence
            # ----------------------------------------

            if pubmed_results:

                article = pubmed_results[0]

                print("\n[6] Sample PubMed Evidence")

                print(
                    f"    PMID: "
                    f"{article.get('pmid', 'N/A')}"
                )

                print(
                    f"    Title: "
                    f"{article.get('title', 'N/A')}"
                )

                print(
                    f"    Journal: "
                    f"{article.get('journal', 'N/A')}"
                )

            if trial_results:

                trial = trial_results[0]

                print("\n[7] Sample Clinical Trial")

                print(
                    f"    NCT ID: "
                    f"{trial.get('nct_id', 'N/A')}"
                )

                print(
                    f"    Title: "
                    f"{trial.get('title', 'N/A')}"
                )

                print(
                    f"    Status: "
                    f"{trial.get('status', 'N/A')}"
                )

            print("\n" + "=" * 60)
            print(" MCP demonstration completed successfully")
            print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
