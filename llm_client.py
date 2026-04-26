import requests

API_KEY = "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"

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