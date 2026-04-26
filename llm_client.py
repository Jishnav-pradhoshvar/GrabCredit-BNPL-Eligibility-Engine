import requests

API_KEY = "YOUR_KEY"

def generate_text(prompt):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-3-haiku",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=5
        )

        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        return None

    except Exception:
        return None
