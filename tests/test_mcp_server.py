import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


server_params = StdioServerParameters(
    command="python",
    args=["-m", "server.server"],
)


def test_mcp_tools_and_prompt():
    asyncio.run(
        _test_mcp_tools_and_prompt()
    )


async def _test_mcp_tools_and_prompt():

    async with stdio_client(
        server_params
    ) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            tools = await session.list_tools()

            tool_names = {
                tool.name
                for tool in tools.tools
            }

            assert "pubmed_search" in tool_names
            assert "pubmed_get_article" in tool_names
            assert "clinical_trials_search" in tool_names
            assert "healthcare_research" in tool_names

            prompts = await session.list_prompts()

            prompt_names = {
                prompt.name
                for prompt in prompts.prompts
            }

            assert "research_brief" in prompt_names


def test_mcp_resource():
    asyncio.run(
        _test_mcp_resource()
    )


async def _test_mcp_resource():

    async with stdio_client(
        server_params
    ) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            resources = await session.list_resources()

            resource_uris = {
                str(resource.uri)
                for resource in resources.resources
            }

            assert (
                "healthcare://research-guidelines"
                in resource_uris
            )

            result = await session.read_resource(
                "healthcare://research-guidelines"
            )

            assert result.contents

            text = str(
                result.contents[0]
            )

            assert (
                "Healthcare Research Server Guidelines"
                in text
            )
