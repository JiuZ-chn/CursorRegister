# Cursor Register

Automatically register a Cursor account and save the account name, password, and token.

## How to use

### Install dependency

The code does not support to run with headless mode now. Please run the python script in Windows platform with UI.

```
pip install requirements.txt
```

### Register accounts. Save the account info and cookie token into csv.
```
python cursor_register.py --number 10
```
- `number` is the account number you want.

### Register accounts. Upload the account cookie token into [One-API](https://github.com/songquanpeng/one-api)
```
python cursor_register.py --oneapi_url {oneapi_url} --oneapi_token {oneapi_token} --oneapi_channel_url {oneapi_channel_url} --oneapi --number 5
```
- `oneapi_url` is the web address for your oneapi server. 
- `oneapi_token` is the access token for your oneapi website. See more details in [OneAPI API](https://github.com/songquanpeng/one-api/blob/main/docs/API.md)
- `oneapi_channel_url` is the cursor-api reverse proxy server like [cursor-api](https://github.com/lvguanjun/cursor-api)

## To do
1. 支持将注册得到的信息上传至数据库
2. 支持根据账号密码刷新Token值

## Thanks
1. 本项目基于[cursor-api](https://github.com/Old-Camel/cursor-api/)中的代码进行优化，感谢原作者的贡献。
