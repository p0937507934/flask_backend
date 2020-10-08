# haoez_api_server
[![pipeline status](https://gitlab.com/nyust-hsipl/cooperation-project/isuzu-optics/haoez_api_server/badges/master/pipeline.svg)](https://gitlab.com/nyust-hsipl/cooperation-project/isuzu-optics/haoez_api_server/-/commits/master) [![coverage report](https://gitlab.com/nyust-hsipl/cooperation-project/isuzu-optics/haoez_api_server/badges/master/coverage.svg)](https://gitlab.com/nyust-hsipl/cooperation-project/isuzu-optics/haoez_api_server/-/commits/master)

:star: 此為與五鈴光學合作之高光譜演算法雲端辨識伺服器

:bulb: 目前支援辨識的儀器
* HP280
* SnapShot

:fire: 預計還會支援的儀器
* NIRez
* ...

:exclamation: 各平台測試狀況

| OS/版本          | Python版本  | 運行狀況           | 備註  |
| -                | -          | -                  | -    |
| Win10/x64        | 3.7.9      | :white_check_mark: |      |
| Win7/X64         | 3.7.9      | :white_check_mark: |      |
| Linux/gitlab-ci  | 3.6.12     | :white_check_mark: |      |
| Ubuntu/?         | ?          | :x:                | #1   |

## 目錄拉
[[_TOC_]]

## 如何使用
0. 載包載起來
```bash
$ git clone '後面自己打'
$ cd haoez_api_server
```

1. 初次建立虛擬環境使用內建venv:
```bash
$ python -m venv env
```

2. 切換到虛擬環境
```bash
# PowerShell
$ .\\env\\Scripts\\Activate.ps1

# cmd:
$ .\\env\\Scripts\\activate.bat
```

> :warning: 執行 Windows PowerShell 的 `.ps1` 指令稿時，出現「系統上已停用指令碼執行」的錯誤訊息
>
> 1. 以系統管理員身分執行`PowerShell`
>
> 2. 執行 `Set-ExecutionPolicy RemoteSigned`

3. 安裝Dependency
```bash
# For 部屬環境：
(env) $ pip install -e .

# For 開發者：
(env) $ pip install -e .["dev"]
```

4. 啟動Server
```bash
(env) $ python .\\haoez_api_server\\__init__.py
```

## Push前準備
* :exclamation: 分支不要在`master`請另開分支，新分支的名稱不要無意義就好
* Commit的格式**盡量**遵照[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)標準
    * 訊息格式
        > 標籤: 訊息
    * 支援的`標籤`請參考`.versionrc`
    * 之前沒遵守的我會想辦法修掉...
* 推到其他分支之後送 MR 給`master`，然後訊息跟我說一下

> :bulb: 遵照`Conventional Commits`其實是為了產生`CHANGELOG.md`，相關說明可以看[這裡](https://linyencheng.github.io/2020/04/25/tool-semantic-version-release/)

## 有新Feature直接更新Issue的TODO
## 有Bug直接開新的Issue