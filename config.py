from datetime import datetime
import os

# 執行當下的時間
DATE = datetime.now().strftime("%Y%m%d_%H%M%S")

# KKGame 管理後台 URL
KK_ADMIN_URL = "https://egame-uat.idc.pstdsf.com"
# KKGame 管理後台語系
KK_ADMIN_LANG = "zh-cn"
# KKGame 管理後台渠道
KK_ADMIN_ECSITE = "1"

#KK後台使用者帳號
KK_ADMIN_USER = 'brent_y'
#KK後台使用者密碼
KK_ADMIN_PASSWORD = '123456'

#KKGame 配牌器 URL
KK_WEBTOOL_URL = "https://webdevtool-uat.idc.pstdsf.com"

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



