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
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.access_token
        }

    def get_channel(self, id):
        url = self.base_url + f"/api/channel/{id}"

        response = requests.get(url, headers=self.headers)
        return response

    def get_channels(self, page, pagesize):
        url = self.base_url + f"/api/channel/?p={page}&page_size={pagesize}"

        response = requests.get(url, headers=self.headers)
        return response

    def add_channel(self, name, base_url, keys, models, rate_limit_count = 0):
        url = self.base_url + "/api/channel"

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

        response = requests.post(url, json=data, headers=self.headers)
        return response
    
    def delete_channel(self, id):
        url = self.base_url + f"/api/channel/{id}"

        response = requests.delete(url, headers=self.headers)
        return response
    
    def enable_channel(self, id):
        url = self.base_url + f"/api/channel"
        data = {
            "id": id,
            "status": 1
        }

        response = requests.put(url, json=data, headers=self.headers)
        return response

    def disable_channel(self, id):
        url = self.base_url + f"/api/channel"
        data = {
            "id": id,
            "status": 2
        }

        response = requests.put(url, json=data, headers=self.headers)
        return response
