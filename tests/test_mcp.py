import asyncio

from app.ai.mcp.client import MCPClient


async def main():

    client = MCPClient(
        command="npx",
        args=[
            "@modelcontextprotocol/server-filesystem",
            r"C:\Temp"
        ]
    )

    print("Connecting to MCP Server...")

    await client.connect()

    print("Connected successfully\n")

    print("Available Tools....")
    print("----------------------------")

    tools = await client.list_tools()

    response = await client.call_tool(
            "read_text_file",
            {
                "path": "sample.txt"
            }
    )

    print(response)
    #print(response.result)

    for tool in tools:
        print(f"Name        : {tool.name}")
        print(f"Description : {tool.description}")
        print(f"Schema      : {tool.input_schema}")
        print()

    await client.disconnect()

    print("Disconnected.")


if __name__ == "__main__":
    asyncio.run(main())