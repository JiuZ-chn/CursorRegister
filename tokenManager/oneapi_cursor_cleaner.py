# The script is used to manage low balance Cursor accounts in one-api service

import argparse

from oneapi_manager import OneAPIManager
from cursor import Cursor

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--oneapi_url', type=str, required=False, help='URL link for One-API website')
    parser.add_argument('--oneapi_token', type=str, required=False, help='Token for One-API website')
    parser.add_argument('--disable_low_balance_accounts', default=False, type=lambda x: (str(x).lower() == 'true'))
    parser.add_argument('--delete_low_balance_accounts', default=False, type=lambda x: (str(x).lower() == 'true'))

    args = parser.parse_args()
    oneapi_url = args.oneapi_url
    oneapi_token = args.oneapi_token
    disable_low_balance_accounts = args.disable_low_balance_accounts 
    delete_low_balance_accounts = args.delete_low_balance_accounts

    oneapi = OneAPIManager(oneapi_url, oneapi_token)

    response_channels = oneapi.get_channels(0, 2147483647)
    channels = response_channels.json()['data']
    channels_id = [channel['id'] for channel in channels]
    print(f"[OneAPI] Channel Count: {len(channels_id)}")

    # Remove channel with low quota
    for id in channels_id:
        key = oneapi.get_channel(id).json()['data']['key']
        remaining_balance = Cursor.get_remaining_balance(key)
        remaining_days = Cursor.get_trial_remaining_days(key)
        print(f"[OneAPI] Channel {id} Info: Balance = {remaining_balance}. Trial Remaining Days = {remaining_days}")
        if None in [remaining_balance, remaining_days]:
            print(f"[OneAPI] Invalid resposne")
            continue
        if remaining_balance < 10:# or remaining_days <= 0:
            if disable_low_balance_accounts:
                response = oneapi.disable_channel(id)
                print(f"[OneAPI] Disable Channel {id}: {response.status_code}")
            if delete_low_balance_accounts:
                response = oneapi.delete_channel(id)
                print(f"[OneAPI] Delete Channel {id}: {response.status_code}")
