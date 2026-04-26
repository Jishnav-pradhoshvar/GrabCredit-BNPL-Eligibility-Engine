import json
import random
from datetime import datetime, timedelta

users = ["U001", "U002", "U003", "U004", "U005"]
categories = ["Electronics", "Fashion", "Grocery", "Travel"]
merchants = ["Amazon", "Flipkart", "Myntra", "Swiggy"]

data = []

def random_date():
    start = datetime(2024, 1, 1)
    return (start + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")

# U001 - New user
for _ in range(2):
    data.append({
        "user_id": "U001",
        "merchant": random.choice(merchants),
        "category": random.choice(categories),
        "gmv": random.randint(200, 1000),
        "coupon_used": False,
        "payment_mode": "UPI",
        "return_flag": False,
        "timestamp": random_date()
    })

# U002 - Low activity
for _ in range(5):
    data.append({
        "user_id": "U002",
        "merchant": random.choice(merchants),
        "category": random.choice(categories),
        "gmv": random.randint(100, 1500),
        "coupon_used": random.choice([True, False]),
        "payment_mode": "UPI",
        "return_flag": False,
        "timestamp": random_date()
    })

# U003 - Medium user
for _ in range(20):
    data.append({
        "user_id": "U003",
        "merchant": random.choice(merchants),
        "category": random.choice(categories),
        "gmv": random.randint(500, 3000),
        "coupon_used": True,
        "payment_mode": "Card",
        "return_flag": False,
        "timestamp": random_date()
    })

# U004 - Power user
for _ in range(120):
    data.append({
        "user_id": "U004",
        "merchant": random.choice(merchants),
        "category": random.choice(categories),
        "gmv": random.randint(1000, 8000),
        "coupon_used": True,
        "payment_mode": "Card",
        "return_flag": False,
        "timestamp": random_date()
    })

# U005 - Risky user
for _ in range(40):
    data.append({
        "user_id": "U005",
        "merchant": random.choice(merchants),
        "category": random.choice(categories),
        "gmv": random.randint(500, 5000),
        "coupon_used": random.choice([True, False]),
        "payment_mode": "UPI",
        "return_flag": random.choice([True, False, True]),  # more returns
        "timestamp": random_date()
    })

with open("mock_transactions.json", "w") as f:
    json.dump(data, f, indent=2)

print("Data generated!")