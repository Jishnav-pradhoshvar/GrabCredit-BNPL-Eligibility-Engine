from datetime import datetime

def check_velocity(user_info: dict):
    if not user_info or "error" in user_info:
        return True, "User not found or invalid data."

    created_at_str = user_info.get("created_at")
    if not created_at_str:
        return True, "Missing creation date."

    try:
        created_at = datetime.strptime(created_at_str, "%Y-%m-%d")
        today = datetime.now()
        days_since_signup = (today - created_at).days

        if days_since_signup < 7:
            return True, f"User registration velocity risk: Account is too new ({days_since_signup} days old). Minimum 7 days required."
    except Exception as e:
        return True, f"Date parsing error: {str(e)}"

    return False, "OK"