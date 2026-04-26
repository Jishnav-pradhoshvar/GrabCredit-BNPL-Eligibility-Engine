from fastapi import APIRouter
import json
import os

router = APIRouter()

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/mock_transactions.json")

@router.get("/transactions/{user_id}")
def get_transactions(user_id: str):
    try:
        with open(DATA_PATH, "r") as f:
            data = json.load(f)

        user_transactions = [
            txn for txn in data if txn["user_id"] == user_id
        ]

        return {
            "user_id": user_id,
            "total_transactions": len(user_transactions),
            "transactions": user_transactions
        }

    except Exception as e:
        return {"error": str(e)}