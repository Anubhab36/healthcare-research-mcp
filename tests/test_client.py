import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


server_params = StdioServerParameters(
    command="python",
    args=["-m", "server.server"],
)


async def main():

    async with stdio_client(
        server_params
    ) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            # --------------------------------
            # Discover tools
            # --------------------------------

            tools = await session.list_tools()

            print("Available tools:")

            for tool in tools.tools:
                print(f"- {tool.name}")

            # --------------------------------
            # Multi-source research
            # --------------------------------

            print("\n--- HEALTHCARE RESEARCH ---")

            result = await session.call_tool(
                "healthcare_research",
                {
                    "query": (
                        "artificial intelligence ECG"
                    ),
                    "max_results": 2,
                },
            )

            research_data = json.loads(
                result.content[0].text
            )

            print(
                json.dumps(
                    research_data,
                    indent=2,
                    ensure_ascii=False,
                )
            )


if __name__ == "__main__":
    asyncio.run(main())
