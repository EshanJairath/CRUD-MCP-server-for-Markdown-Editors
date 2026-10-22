from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# creating a server instance
app = Server('my-server')

# declaring all the available tools in the server
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name='add',
            description='Adds two numbers',
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        ),
        # adding subtract tool for demonstration
        Tool(
            name='subtract',
            description='Subtracts two numbers',
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        ),

        Tool(
            name='multiply',
            description='Multiplies two numbers',
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        ),

        Tool(name = 'divide',
             description = 'Divides two numbers',
             inputSchema={
                 "type": "object",
                 "properties": {
                     "a": {"type": "number", "description": "First number"},
                     "b": {"type": "number", "description": "Second number"}
                 },
                 "required": ["a", "b"]
             }),

        Tool(name = 'percentage',
             description = 'Calculates percentage of 2 numbers',
             inputSchema={
                 "type": "object",
                 "properties": {
                     "a": {"type": "number", "description": "First number"},
                     "b": {"type": "number", "description": "Second number"}
                 },
                 "required": ["a", "b"]
             })
    ]

# handling the tool calls
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == 'add':
        result = arguments['a'] + arguments['b']
        return [TextContent(type='text', text=str(result))]
    if name == 'subtract':
        result = arguments['a'] - arguments['b']
        return [TextContent(type='text', text=str(result))]
    if name == 'multiply':
        result = arguments['a'] * arguments['b']
        return [TextContent(type='text', text=str(result))]
    if name == 'divide':
        result = arguments['a'] / arguments['b']
        return [TextContent(type='text', text=str(result))]
    if name == 'percentage':
        result = (arguments['a'] / arguments['b']) * 100
        return [TextContent(type='text', text=str(result))]
    raise ValueError(f"Tool {name} not found")


# running the server
if __name__ == "__main__":
    import asyncio

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )

    asyncio.run(main())