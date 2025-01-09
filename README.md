<p align="center">
  <span>
   English | 
   <a href="https://github.com/JiuZ-Chn/CursorRegister/blob/main/README.zh_CN.md">简体中文</a>
  </span>
<p>

# Cursor Register

Automatically register a Cursor account and save the account name, password, and token.

Poor network environment has a huge impact on this project. If the registration success rate is low, please consider using a proxy or other network. We provide Github Action pipeline for trial use.
（较差的网络环境对本项目影响巨大，如果注册成功率较低，请考虑使用代理或者使用其他网络，本项目提供Github Action pipeline以供试用）

## Feature

- Register Cursor accounts and save account, password and token to .csv locally. (注册Cursor账号并保存账号密码Token到本地)
- Register Cursor accounts upload tokens to One API. (注册Cursor账号并上传Token到One API)
- Clean up Cursor channels with low balance in One API. (清理One API中额度不足的Cursor账号)
- The above features all support to run in Github Action environment. (上述功能均支持Github Action环境)

## Run in local

### Install dependency **(It's required to use `Python >= 3.10`)**

The code does not support to run with headless mode now. Please run the python script in Windows platform with UI. 

```
pip install -r requirements.txt
```

### Register accounts. Save the account info and cookie token into csv.

```
python cursor_register.py --number 3
```
- `number`: The account number you want to register

### Register accounts. Upload the account cookie token into [One-API](https://github.com/songquanpeng/one-api)

```
python cursor_register.py --oneapi_url {oneapi_url} --oneapi_token {oneapi_token} --oneapi_channel_url {oneapi_channel_url} --oneapi --number 5
```
- `oneapi_url`: The web address for your oneapi server. 
- `oneapi_token`: The access token for your oneapi website. See more details in [OneAPI API](https://github.com/songquanpeng/one-api/blob/main/docs/API.md)
- `oneapi_channel_url`: The cursor-api reverse proxy server like [cursor-api](https://github.com/lvguanjun/cursor-api)

### Clean up low balance Cursor channels in [One-API](https://github.com/songquanpeng/one-api)

```
python tokenManager/oneapi_cursor_cleaner.py --oneapi_url {oneapi_url} --oneapi_token {oneapi_token}
```
- `oneapi_url`: The web address for your oneapi server. 
- `oneapi_token`: The access token for your oneapi website. See more details in [OneAPI API](https://github.com/songquanpeng/one-api/blob/main/docs/API.md)

## Run in Github Action

### Register accounts. Download account info and cookie token from Github Artifact.

If you want to use the token directly or your OneAPI does not have a public IP, you can manually download `token.csv` after running the GitHub Action pipeline. **Do not forget to delete the artifact after you download it to avoid data leakage.**

Please run the Github Action pipeline **`Cursor Register`** with the following parameter:
- `number`: The account number you want to register.
- `max_workers`: Parallelism for threading pool. Suggest to use `1` in Github Action environment.
- `Ingest account tokens to OneAPI`: Mark as `☐` to disable One-API service.
- `Upload account infos to artifact`: Mark as `☑` to make Github Action uploead the csv files to artifacts. Then you can download them after workflow succeeds.

### Register accounts. Upload the account cookie token into [One-API](https://github.com/songquanpeng/one-api)

Before ingest the account cookie into ONE API, you need to add the following secret in your repo. If you are new to use secret in Github Action. you can add the secret following [Security Guides](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository) 

- `CURSOR_ONEAPI_URL`: For parameter `oneapi_url`
- `CURSOR_ONEAPI_TOKEN`: For parameter `oneapi_token`
- `CURSOR_CHANNEL_URL`: For parameter `oneapi_channel_url`

Please run the Github Action pipeline **`Cursor Register`** with the following parameter:
- `number`: The account number you want to register.
- `max_workers`: Parallelism for threading pool. Suggest to use `1` in Github Action environment.
- `Ingest account tokens to OneAPI`: Mark as `☑` to enable One-API service.
- `Upload account infos to artifact`: `☑` for uploeading the artifact and `☑` will skip this step

### Clean up low balance Cursor channels in [One-API](https://github.com/songquanpeng/one-api)

Please run the Github Action pipeline **`OneAPI Cursor Cleaner`**. Before runnign the pipeline, you need to add the following secrets in your repo.

- `CURSOR_ONEAPI_URL`: For parameter `oneapi_url`
- `CURSOR_ONEAPI_TOKEN`: For parameter `oneapi_token`

## Todo
- Maybe some bugs when running in multiple threading mode (`max_workers` > 1), but not sure. :(
- A new Github Action pipeline to automatically maintain the minimum balance of Curosr accounts in OneAPI, and automatically register if the balance is too low.

## Thanks
- [cursor-api](https://github.com/Old-Camel/cursor-api/) for Python code in auto register
