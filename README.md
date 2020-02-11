# haoez_api_server

## 初次使用
### 1. 使用virtualenv建立虛擬環境
* 安裝: `pip install virtualenv`
* 建立: `virtualenv env`
### 2. 安裝Dependency
* For usr: `pip install .`
* For dev: `pip install -e .["dev"]`

## 上傳前準備
* 分支要在`feat`
* 遵照[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)標準
* 推上去之前要先跑測試!!!!
    * `coverage run -m pytest`

## 遇到PowerShell指令問題
> 執行 Windows PowerShell 的 `.ps1` 指令稿時，出現「系統上已停用指令碼執行」的錯誤訊息

#### 解法:
1. 以系統管理員身分執行`PowerShell`
2. 執行 `Set-ExecutionPolicy RemoteSigned`
3. Done!!