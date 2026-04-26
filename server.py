from mcp.server.fastmcp import FastMCP
import json
import os

mcp = FastMCP("GrabOn")

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/mock_transactions.json"))
USERS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/users.json"))

@mcp.tool()
def get_user_transactions(user_id: str) -> list[dict]:
    """Get all past transactions for a specific GrabOn user."""
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return [t for t in data if t["user_id"] == user_id]

@mcp.tool()
def get_user_data(user_id: str) -> dict:
    """Get user creation data and basic profile for a GrabOn user."""
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        users = json.load(f)
    user = next((u for u in users if u["user_id"] == user_id), None)
    return user or {"error": "User not found"}

if __name__ == "__main__":
    mcp.run()
