import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
import os

SERVER_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), "mcp_server", "server.py"))

async def fetch_user_data_via_mcp(user_id: str):
    server_params = StdioServerParameters(
        command="python",
        args=[SERVER_SCRIPT],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Call tools
            tx_result = await session.call_tool("get_user_transactions", arguments={"user_id": user_id})
            usr_result = await session.call_tool("get_user_data", arguments={"user_id": user_id})
            
            transactions = tx_result.content[0].text if tx_result.content else "[]"
            user_info = usr_result.content[0].text if usr_result.content else "{}"
            
            import json
            try:
                transactions = json.loads(transactions)
            except:
                pass
                
            try:
                user_info = json.loads(user_info)
            except:
                pass
                
            return transactions, user_info
