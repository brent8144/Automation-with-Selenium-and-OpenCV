"# Automation-with-Selenium-and-OpenCV" 

- [Automation with Selenium and OpenCV](#automation-with-selenium-and-opencv)
  - [Summary](#summary)
  - [Quick Start](#quick-start)
      - [安裝 Python Modules](#安裝-python-modules)
  - [調整相關參數](#調整相關參數)
      - [Step.1 Config](#step1-config)
      - [Step.2 執行程式](#step2-執行程式)
  - [Project Layout](#project-layout)
  - [執行結果](#執行結果)
      - [測試報告](#測試報告)

--- 

## Summary

自動化測試腳本，利用 Selenium 及 OpenCV 進行電子遊戲的回歸測試。

---

## Quick Start

### 安裝 Python Modules

首次下載該專案時，可以執行該指令安裝該專案所需使用到的第三方模組

```shell
make install_requirements
```

---

## 調整相關參數
修改圖片存放路徑 & driver位置 & 報告存放路徑 `config.py`

### Step.1 Config

```python
# KKGame 管理後台 URL
KK_ADMIN_URL = "測試網站網址"
# KKGame 管理後台語系
KK_ADMIN_LANG = "zh-cn"
# KKGame 管理後台渠道
KK_ADMIN_ECSITE = "1"

#KK後台使用者帳號
KK_ADMIN_USER = '後台使用者帳號'
#KK後台使用者密碼
KK_ADMIN_PASSWORD = '後台使用者密碼'

#KKGame 配牌器 URL
KK_WEBTOOL_URL = "配牌器網址"

# 專案根目錄路徑
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# 提供整合測試報告的根目錄路徑
REPORT_ROOT_DIR = os.path.join(BASE_DIR, "KKGAME_REPORT")
# 測試報告位置
REPORT_GEN_DIR = os.path.join(REPORT_ROOT_DIR, f"kkgame_report_{DATE}")

# 提供原圖片的保存路徑
GROUND_TRUTU_DIR = os.path.join(BASE_DIR, "KKGAME_PIC")
# 提通截圖的保存路徑
BACKGROUND_SPACE = os.path.join(BASE_DIR, "KKGAME_PIC_BACKGROUND")
# 提供比對後結果的保存路徑
VS_SPACE = os.path.join(BASE_DIR, "KKGAME_PIC_VS")

#chrome driver位置
CHROME_DRIVER_DIR = os.path.join(BASE_DIR, "BIN", "chromedriver.exe")
```

### Step.2 執行程式

執行測試腳本 `kkgame_slot_regression.py`

**註1:**  

BeautifulReport如果為0.0.4以後的版本，需將 `log_path` 變更為 `report_dir`

```python
BeautifulReport(testunit).report(
        filename = f"kkgame_report_{config.DATE}", 
        description = f"KKGAME_測試報告({config.DATE})", 
        log_path = config.REPORT_GEN_DIR
    )
```

---

## Project Layout

```text
KKGame Slot Regression Testing Tool
 ├─ BIN/                      # driver
 ├─ GAME/                     # 遊戲
 ├─ KKGAME_PIC/               # 原圖存放位置
 ├─ KKGAME_PIC_BACKGROUND/    # 擷圖存放位置
 ├─ KKGAME_PIC_VS/            # 比對後圖片存放位置
 ├─ KKGAME_REPORT/            # 報告存放位置
 ├─ pic/                      # 
 ├─ ..                        #
 ├─ config.py                 # 設定檔
 ├─ util.py                   # 
 ├─ pictest.py                # 圖片比對
 ├─ kkgame_slot_regression.py # Automation
 ├─ ..                        #
 ├─ README.md                 # 
 ├─ requirements.txt          # 該專案所依賴的 python 第三方模組列表
 ├─ .gitignore                #
```

---

## 執行結果

### 測試報告

![image](https://github.com/brent8144/Automation-with-Selenium-and-OpenCV/blob/main/pic/report.PNG)
