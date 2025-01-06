import os
import re
import csv
import argparse
import concurrent.futures
from datetime import datetime
from faker import Faker
from tempmail import EMail
from DrissionPage import ChromiumOptions, Chromium

CURSOR_LOGIN_URL = "https://authenticator.cursor.sh"
CURSOR_SIGN_UP_URL =  "https://authenticator.cursor.sh/sign-up"
CURSOR_SETTINGS_URL = "https://www.cursor.com/settings"

hide_account_info = os.getenv('HIDE_ACCOUNT_INFO', 'false').lower() == 'true'

def cursor_turnstile(tab, retry_times = 5):
    for _ in range(retry_times): # Retry times
        try:
            challenge_shadow_root = tab.ele('@id=cf-turnstile').child().shadow_root
            challenge_shadow_button = challenge_shadow_root.ele("tag:iframe", timeout=30).ele("tag:body").sr("xpath=//input[@type='checkbox']")
            if challenge_shadow_button:
                challenge_shadow_button.click()
                tab.wait.load_start()
                break
        except:
            pass
        if _ == retry_times - 1:
            print("[Register] Timeout when passing turnstile")

def sign_up(browser):

    retry_times = 5
    
    # Get temp email address
    temp_email = EMail()
    email = temp_email.address

    # Get password and name by faker
    fake = Faker()
    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
    first_name, last_name = fake.name().split(' ')[0:2]

    tab = browser.new_tab(CURSOR_SIGN_UP_URL)
    browser.wait(0.5, 1.5)
    # Input first name, last name, email
    for _ in range(retry_times):
        try:
            tab.ele("xpath=//input[@name='first_name']").input(first_name, clear=True)
            tab.ele("xpath=//input[@name='last_name']").input(last_name, clear=True)
            tab.ele("xpath=//input[@name='email']").input(email, clear=True)
            tab.ele("@type=submit").click()
            tab.wait(2.5, 4.5)

            if tab.ele("xpath=//input[@name='email']").attr("data-valid") != "true":
                tab.close()
                return None

        except Exception as e:
            print(e)
            tab.close()
            return None
        
        # In password page or data is validated, continue to next page
        if tab.ele("xpath=//input[@name='password']") or tab.ele("xpath=//input[@name='email']").attr("data-valid") is not None:
            break

        # Kill the function since time out 
        if _ == retry_times -1:
            print("[Register] Timeout when inputing email address")
            tab.close()
            return None

    # If not in password page, try pass turnstile page
    if not tab.ele("xpath=//input[@name='password']"):
        cursor_turnstile(tab)
    
    # Input password
    for _ in range(retry_times):
        try:
            tab.ele("xpath=//input[@name='password']").input(password, clear=True)
            tab.ele('@type=submit').click()
            tab.wait(2.5, 4.5)
        except Exception as e:
            print(e)
            tab.close()
            return None

        # In code verification page or data is validated, continue to next page
        if tab.ele("xpath=//input[@data-index=0]") or tab.ele("xpath=//input[@name='password']").attr("data-valid") is not None:
            break

        # Kill the function since time out 
        if _ == retry_times -1:
            print("[Register] Timeout when inputing password")
            tab.close()
            return None

    # If not in verification code page, try pass turnstile page
    if not tab.ele("xpath=//input[@data-index=0]"):
        cursor_turnstile(tab)

    # Input email verification code
    try:
        message = temp_email.wait_for_message(timeout=120)
        message_text = message.body.strip().replace('\n', '').replace('\r', '').replace('=', '')
        verify_code = re.search(r'Your verification code is (\d+)', message_text).group(1).strip()
        for idx, digit in enumerate(verify_code, start = 0):
            tab.ele(f"xpath=//input[@data-index={idx}]", timeout=30).input(digit, clear=True)
            tab.wait(0.1, 0.3)
        tab.wait(0.5, 1.5)            
    except Exception as e:
        print(e)
        tab.close()
        return None

    if tab.url != "https://www.cursor.com/":
        cursor_turnstile(tab)

    # Get cookie
    cookies = tab.cookies().as_dict()
    token = cookies.get('WorkosCursorSessionToken', None)
    tab.close()

    if not hide_account_info:
        print("[Register] Cursor Email: " + email)
        print("[Register] Cursor Password: " + password)
        print("[Register] Cursor Token: " + token)
    return {
        'username': email,
        'password': password,
        'token': token
    }

def register_cursor(number, max_workers):

    options = ChromiumOptions()
    options.auto_port()
    #options.headless()

    # Use turnstilePatch from https://github.com/TheFalloutOf76/CDP-bug-MouseEvent-.screenX-.screenY-patcher
    options.add_extension("turnstilePatch")
    browser = Chromium(options)

    # Run the code using multithreading
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(sign_up, browser) for _ in range(number)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                results.append(result)
    browser.quit(force=True)

    results = [result for result in results if result["token"] is not None]
    #print(results)
    if len(results)>0:
        formatted_date = datetime.now().strftime("%Y-%m-%d")

        csv_file = f"./output_{formatted_date}.csv"
        token_file = f"./token_{formatted_date}.csv"

        fieldnames = results[0].keys()

        # Write username, password, token into a csv file
        with open(csv_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not os.path.isfile(csv_file): writer.writeheader()
            writer.writerows(results)

        # Only write token to csv file, without header
        tokens = [{'token': row['token']} for row in results]
        with open(token_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['token'])
            writer.writerows(tokens)

    return results

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Cursor Registor')
    parser.add_argument('--number', type=int, default=2, help="How many account you want")
    parser.add_argument('--max_workers', type=int, default=1, help="How many workers in multithreading")
    
    # The parameters with name starts with oneapi are used to uploead the cookie token to one-api, new-api, chat-api server.
    parser.add_argument('--oneapi', action='store_true', help='Enable One-API or not')
    parser.add_argument('--oneapi_url', type=str, required=False, help='URL link for One-API website')
    parser.add_argument('--oneapi_token', type=str, required=False, help='Token for One-API website')
    parser.add_argument('--oneapi_channel_url', type=str, required=False, help='Base url for One-API channel')

    args = parser.parse_args()
    number = args.number
    max_workers = args.max_workers
    use_oneapi = args.oneapi
    oneapi_url = args.oneapi_url
    oneapi_token = args.oneapi_token
    oneapi_channel_url = args.oneapi_channel_url

    account_infos = register_cursor(number, max_workers)
    print(f"[Register] Register {len(account_infos)} Accounts Successfully")
    
    if use_oneapi and len(account_infos)>0:
        from tokenManager.oneapi_manager import OneAPIManager
        oneapi = OneAPIManager(oneapi_url, oneapi_token)
        response = oneapi.add_channel("Cursor",
                                      oneapi_channel_url,
                                      [row['token'] for row in account_infos],
                                      OneAPIManager.cursor_models)
        print(f'[OneAPI] Add Channel Request Status Code: {response.status_code}')
        print(f'[OneAPI] Add Channel Request Response Body: {response.json()}')
