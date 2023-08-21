import logging
import os
import sys
sys.path.append(r'C:\Users\brent_yang\Desktop\Selenium')
import unittest
from webbrowser import Chrome
from xml.dom import DOMException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
import BeautifulReport
from BeautifulReport import BeautifulReport
import pictest 
import pyautogui
import matplotlib.pyplot as plt
import config
import util

HTML_IMG_TEMPLATE = """
    <a href="data:image/png;base64, {}" target="_blank" rel="external nofollow" >
    <img src="data:image/png;base64, {}" width="800px" height="500px"/>
    </a>
    <br></br>
"""
class G64Tester(unittest.TestCase):

    # chrome driver位置
    driver_space = config.CHROME_DRIVER_DIR

    # 特徵點
    feature = 170

    # 截圖等待時間(sec)
    pic_sleep = 5

    # 滑鼠點擊取消新手教學(滑鼠移動座標) 1.麻將 2.森林舞會
    new_mousemove_mahjong = 392,649
    new_mousemove_forest = 700,179
    # 滑鼠點擊取確認作弊器(滑鼠移動座標)
    new_mousemove_confirm = 680,185
    # spin
    spin = 855,701

    @classmethod
    def setUpClass(cls):
        # Selenium
        # 取消網頁中的彈出視窗，避免妨礙網路爬蟲的執行
        options = Options()
        options.add_argument("--disable-notifications")
        # 引用webdriver
        cls.chrome = webdriver.Chrome(cls.driver_space, chrome_options=options)       
        # 設定遊戲ID
        cls.GAME_ID = "64"
        # 等待時間
        cls.WEBDRIVER_TIMEOUT = 10 # WebDriverWait 的條件等待時間
        cls.LOADING_DELAY = 5
        cls.SPIN_DELAY = 5
        # 設定配牌器
        cls.cheat_table = {
            "params": {
                "key": f"{config.KK_ADMIN_USER}-{cls.GAME_ID}", 
                "data": {
                    "baseGame": [2, 8, 35, 198, 147], 
                    "longWildIndex": -1, 
                    "cheatCase": 0
                }
            }
        }
        
        time.sleep(3)

    @classmethod
    def tearDownClass(self):
        # 所有case跑完後就退出瀏覽器
        self.chrome.quit()
        #pass

    def test_01_update_cheat_table(self):
        '''更新配牌器'''
        resp = util.update_slot_cheat_table(config.KK_WEBTOOL_URL, self.cheat_table)
        if resp == "":
            raise RuntimeError("配牌器更新失敗")
        else:
            print("G"+self.GAME_ID+"配牌器更新成功")
        
    def test_02_opengame(self):
        """
        TestCase 進入 KKGame 指定遊戲, 進行下注後對螢幕截圖
        """

        # 取得操作 KKGame 管理後台的操作憑證
        token = util.get_kkgame_admin_access_token(
            config.KK_ADMIN_URL,
            config.KK_ADMIN_USER,
            config.KK_ADMIN_PASSWORD,
        )
        
        # 取得指定遊戲連結
        url = util.get_kkgame_game_url(
            config.KK_ADMIN_URL,
            token,
            self.GAME_ID,
            config.KK_ADMIN_ECSITE,
            config.KK_ADMIN_LANG,
        )

        # 跳轉到指定遊戲
        self.chrome.get(url)

        # 等待遊戲加載完成
        WebDriverWait(self.chrome, self.WEBDRIVER_TIMEOUT).until(util.waiting_cocos_loading)

        # 跳轉場景過程沒辦法用其他方式判斷, 只能強制等待
        time.sleep(self.LOADING_DELAY)
        
    def test_03_vsgame(self):    
        """
        比對結果
        """
        pyautogui.moveTo(self.spin)
        pyautogui.click()
        time.sleep(self.SPIN_DELAY)

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), config.BACKGROUND_SPACE, "background_g"+self.GAME_ID+".png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''圖像比對'''
        img1 = config.BACKGROUND_SPACE + ("/background_g"+self.GAME_ID+".png")
        img2 = config.GROUND_TRUTU_DIR + ("/g"+self.GAME_ID+".png")
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(config.VS_SPACE + ("/vs_g"+self.GAME_ID+".png"),getimage)
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<span class = blue-bg1><br>實際畫面 ---></span>")
            print("<img src='" + img1 + "'width=300 />")
            print("<span class = blue-bg1><br>原圖 --->")
            print("<img src='" + img2 + "'width=300 />")
            self.chrome.back()
        elif 0 <= pic < 5:
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message ="<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖完全不符</span>" 
            print("<span class = blue-bg1><br>實際畫面 ---></span>")
            print("<img src='" + img1 + "'width=600 />")
            print("<span class = blue-bg1>原圖 ---></span>")
            print("<img src='" + img2 + "'width=600 />")
            raise DemoException(message)
        else:
            plt.imsave(config.VS_SPACE + ("/vs_g"+self.GAME_ID+"_fail.png"),getimage)
            picdata_fail=config.VS_SPACE + ("/vs_g"+self.GAME_ID+"_fail.png")
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
            
 
# BeautifulReport測試報告
if __name__ == '__main__':
    # 檢查所需資料夾是否存在
    if not os.path.exists(config.GROUND_TRUTU_DIR):
        os.mkdir(config.GROUND_TRUTU_DIR)
    if not os.path.exists(config.REPORT_ROOT_DIR):
        os.mkdir(config.REPORT_ROOT_DIR)
    
    # 建立這次測試的報告路徑
    os.mkdir(config.REPORT_GEN_DIR)

    testunit = unittest.TestSuite()
    # 載入用例
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G64Tester))
    result = BeautifulReport(testunit)
    # 輸出報告
    result.report(
        filename = f"kkgame_report_{config.DATE}",
        description = f"KKGAME_測試報告({config.DATE})", 
        log_path=config.REPORT_GEN_DIR
    )