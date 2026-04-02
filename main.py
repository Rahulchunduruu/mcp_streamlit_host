from config import Config
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage

import json
import asyncio
import os


SERVERS = {
    "expense": {
        "transport": "streamable_http",  # if this fails, try "sse"
        "url": Config.expense_server_url,
        "headers":{
            "Authorization": Config.horizon_api_key
                 }
        }
    }


async def main(prompt):
    # Initialize the MCP client
    mcp_client = MultiServerMCPClient(SERVERS)
    tools = await mcp_client.get_tools()

    print("Tools fetched from MCP servers:")
    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool

    #print("Available tools:", list(named_tools.keys()))

    # Initialize the OpenAI client
    llm = ChatOpenAI(model="gpt-5", api_key=Config.OPENAI_API_KEY)
    llm_with_tools = llm.bind_tools(tools)

    # Example user query
    response = await llm_with_tools.ainvoke(prompt)
    print('Initial response from LLM:', response)

    tool_messages = []
    for tc in response.tool_calls:
        selected_tool = tc["name"]
        selected_tool_args = tc.get("args") or {}
        selected_tool_id = tc["id"]

        result = await named_tools[selected_tool].ainvoke(selected_tool_args)
        tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))

    final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
    print('Final response from LLM after tool calls:', final_response)
    return final_response.content

if __name__ == "__main__":
     prompt = "Give summary of expenses for last year to till now and categorize them."
     asyncio.run(main(prompt))