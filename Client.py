import asyncio
from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from config import MODEL
import json


async def main():
    server_params = StdioServerParameters(
        command="python", 
        args=["Server.py"] 
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1. Get tools from MCP server
            tools_result = await session.list_tools()
            azure_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    },
                }
                for tool in tools_result.tools
            ]

            # Connect to local LLM (e.g., Ollama, LM Studio)
            client = AsyncOpenAI(
                base_url="http://127.0.0.1:1234/v1",
                api_key="sk-not-needed"  # Local servers typically don't require auth
            )

            # 2. Initialize Conversation History
            messages = [
                {"role": "system", "content": "You are a helpful assistant with access to a filesystem note-taking tool. You can create, read, update, delete, and email notes."}
            ]

            print("\n=== MCP Chat Interface Active ===")
            print("Type 'exit' or 'quit' to stop.\n")

            # 3. Start the Chat Loop
            while True:
                user_input = input("You: ")
                if user_input.lower() in ['exit', 'quit']:
                    break

                messages.append({"role": "user", "content": user_input})

                # 4. Process the AI's response (and potential tool calls)
                while True:
                    response = await client.chat.completions.create(
                        model=MODEL,
                        messages=messages,
                        tools=azure_tools,
                        tool_choice="auto"
                    )

                    response_message = response.choices[0].message
                    
                    # If there's content in the message, add it to history
                    if response_message.content:
                        messages.append({"role": "assistant", "content": response_message.content})
                    else:
                        # Append the message anyway to maintain tool call structure
                        messages.append(response_message)

                    # If the AI responded with text and NO tool calls, show the text and wait for user
                    if not response_message.tool_calls:
                        print(f"\nAI: {response_message.content}\n")
                        break

                    # Process tool calls if present
                    for tool_call in response_message.tool_calls:
                        name = tool_call.function.name
                        args = json.loads(tool_call.function.arguments)
                        
                        print(f"  [SYSTEM] Calling tool: {name}...")
                        
                        result = await session.call_tool(name, args)
                        tool_result_text = result.content[0].text
                        
                        print(f"  [SERVER] Result: {tool_result_text}")

                        # Feed result back to conversation
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": name,
                            "content": tool_result_text,
                        })
                    
                    # Loop back to let the LLM see the tool result and decide its next move


if __name__ == "__main__": # did the code run directly (vs imported as a module)?
    asyncio.run(main())





























    # # 1. Setup the connection to the MCP server
    # server_params = StdioServerParameters(
    #     command="python", 
    #     args=["Server.py"] 
    # )

    # async with stdio_client(server_params) as (read, write):
    #     async with ClientSession(read, write) as session:
    #         await session.initialize()

    #         # 2. Get tools from MCP server and format for Azure
    #         tools_response = await session.list_tools()
    #         azure_tools = [
    #             {
    #                 "type": "function",
    #                 "function": {
    #                     "name": tool.name,
    #                     "description": tool.description,
    #                     "parameters": tool.inputSchema
    #                 },
    #             }
    #             for tool in tools_response.tools
    #         ]

    #         # 3. Setup Azure OpenAI Client
    #         client = AsyncAzureOpenAI(
    #             azure_endpoint=RESOURCE_ENDPOINT,
    #             api_key=API_KEY,
    #             api_version=API_VERSION
    #         )

    #         # 4. Define the conversation
    #         user_prompt = "Create a detailed markdown file called about this new Ai thing called N8N how it works. Then list all my notes to confirm it is there."
    #         messages = [{"role": "user", "content": user_prompt}]

    #         # 5. THE TOOL LOOP: Allow the LLM to call tools until it's finished
    #         while True:
    #             response = await client.chat.completions.create(
    #                 model=MODEL,
    #                 messages=messages,
    #                 tools=azure_tools,
    #                 tool_choice="auto"
    #             )

    #             response_message = response.choices[0].message
    #             messages.append(response_message) # Add LLM response to history

    #             # If the LLM doesn't want to call a tool, it's done
    #             if not response_message.tool_calls:
    #                 print(f"\nAI Response: {response_message.content}")
    #                 break

    #             # Process tool calls
    #             for tool_call in response_message.tool_calls:
    #                 name = tool_call.function.name
    #                 # Use json.loads instead of eval for safety
    #                 args = json.loads(tool_call.function.arguments)
                    
    #                 print(f"\n[SYSTEM] LLM calling tool: {name} with args: {args}")
                    
    #                 # Call the MCP server
    #                 result = await session.call_tool(name, args)
    #                 tool_result_text = result.content[0].text
    #                 print(f"[SERVER] {tool_result_text}")

    #                 # Feed the tool result back to the LLM
    #                 messages.append({
    #                     "tool_call_id": tool_call.id,
    #                     "role": "tool",
    #                     "name": name,
    #                     "content": tool_result_text,
    #                 })
