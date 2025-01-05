import requests

class OneAPIManager:
    
    cursor_models = ["claude-3-5-sonnet-20241022", 
                              "claude-3-opus", 
                              "claude-3-5-haiku", 
                              "claude-3-5-sonnet", 
                              "cursor-small", 
                              "gemini-exp-1206",
                              "gemini-2.0-flash-exp",
                              "gemini-2.0-flash-thinking-exp",
                              "gpt-3.5-turbo",
                              "gpt-4",
                              "gpt-4-turbo-2024-04-09",
                              "gpt-4o",
                              "gpt-4o-mini",
                              "o1-mini",
                              "o1-preview"]

    def __init__(self, url, access_token):
        self.base_url = url
        self.access_token = access_token

    def add_channel(self, name, base_url, keys, models, rate_limit_count = 0):
        url = self.base_url + "/api/channel"

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.access_token
        }

        data = {"name": name,
                "type": 1,
                "key": "\n".join(keys),
                "openai_organization": "",
                "base_url": base_url,
                "other": "",
                "model_mapping":"",
                "status_code_mapping":"",
                "headers":"",
                "models": ','.join(models),
                "auto_ban":0,
                "is_image_url_enabled": 0,
                "model_test": models[0],
                "tested_time": 0,
                "priority": 0,
                "weight": 0,
                "groups": ["default"],
                "proxy_url": "",
                "region": "",
                "sk": "",
                "ak": "",
                "project_id": "",
                "client_id": "",
                "client_secret": "",
                "refresh_token": "",
                "gcp_account": "",
                "rate_limit_count":rate_limit_count,
                "gemini_model":"",
                "tags":"Cursor",
                "rate_limited":rate_limit_count>0,
                "is_tools": False,
                "claude_original_request": False,
                "group":"default"
        }

        response = requests.post(url, json=data, headers=headers)
        print(f'OneAPI Request Status Code: {response.status_code}')
        print(f'OneAPI Request Response Body: {response.json()}')
