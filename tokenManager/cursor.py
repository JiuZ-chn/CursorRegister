import requests

class Cursor:

    @classmethod
    def get_remaining_balance(cls, token):
        user = token.split("%3A%3A")[0]
        url = f"https://www.cursor.com/api/usage?user={user}"

        headers = {
            "Content-Type": "application/json",
            "Cookie": f"WorkosCursorSessionToken={token}"
        }
        response = requests.get(url, headers=headers)
        usage = response.json().get("gpt-4", None)
        if usage is None or "maxRequestUsage" not in usage or "numRequests" not in usage:
            return None
        return usage["maxRequestUsage"] - usage["numRequests"]

    @classmethod
    def get_trial_remaining_days(cls, token):
        url = f"https://www.cursor.com/api/auth/stripe"

        headers = {
            "Content-Type": "application/json",
            "Cookie": f"WorkosCursorSessionToken={token}"
        }
        response = requests.get(url, headers=headers)
        remaining_days = response.json().get("daysRemainingOnTrial", None)
        return remaining_days
