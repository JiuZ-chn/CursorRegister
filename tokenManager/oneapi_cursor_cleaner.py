# The code is used to delete low quota cursor account in one-api service

import argparse
import requests
from oneapi_manager import OneAPIManager

class Cursor:

    def __init__():
        pass

    @classmethod
    def get_remaining_quota(cls, token):
        user = token.split("%3A%3A")[0]
        url = f"https://www.cursor.com/api/usage?user={user}"

        headers = {
            "Content-Type": "application/json",
            "Cookie": f"WorkosCursorSessionToken={token}"
        }
        response = requests.get(url, headers=headers)
        usage = response.json()["gpt-4"]
        return usage["maxRequestUsage"] - usage["numRequests"]

    @classmethod
    def get_trial_remaining_days(cls, token):
        user = token.split("%3A%3A")[0]
        url = f"https://www.cursor.com/api/auth/stripe"

        headers = {
            "Content-Type": "application/json",
            "Cookie": f"WorkosCursorSessionToken={token}"
        }
        response = requests.get(url, headers=headers)
        remaining_days = response.json().get("daysRemainingOnTrial", -1)
        return remaining_days


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--oneapi_url', type=str, required=False, help='URL link for One-API website')
    parser.add_argument('--oneapi_token', type=str, required=False, help='Token for One-API website')

    args = parser.parse_args()
    oneapi_url = args.oneapi_url
    oneapi_token = args.oneapi_token

    oneapi = OneAPIManager(oneapi_url, oneapi_token)

    response_channels = oneapi.get_channels(0, 2147483647)
    channels = response_channels.json()['data']
    channels_id = [channel['id'] for channel in channels]
    print(f"[OneAPI] Channel Count: {len(channels_id)}")

    # Remove channel with low quota
    for id in channels_id:
        key = oneapi.get_channel(id).json()['data']['key']
        remaining_quota = Cursor.get_remaining_quota(key)
        remaining_days = Cursor.get_trial_remaining_days(key)
        print(f"[OneAPI] Channel {id} Info: Quota = {remaining_quota}. Trial Remaining Days = {remaining_days}")
        if remaining_quota < 10:# or remaining_days <= 0:
            quota = oneapi.delete_channel(id)
            print(f"[OneAPI] Channel {id} Is Deleted.")
