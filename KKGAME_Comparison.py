import logging
import os
import sys
import unittest
from webbrowser import Chrome
from xml.dom import DOMException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import BeautifulReport
from BeautifulReport import BeautifulReport
import pictest 
import pyautogui
import matplotlib.pyplot as plt
import config

HTML_IMG_TEMPLATE = """
    <a href="data:image/png;base64, {}" target="_blank" rel="external nofollow" >
    <img src="data:image/png;base64, {}" width="800px" height="500px"/>
    </a>
    <br></br>
"""

# 版本
version = "20221227.0"
# 報告存放位置

class Test(unittest.TestCase):

    # chrome driver位置
    driver_space = config.driver_space
    # 原圖存放位置
    ori_space = config.ori_space
    # 擷取圖片存放位置
    background_space = config.background_space
    # 比對圖片存放位置
    vs_space = config.vs_space 

    # 特徵點
    feature = 300

    # 啟動遊戲等待時間(sec)
    open_sleep = 20
    # 截圖等待時間(sec)
    pic_sleep = 5

    # 滑鼠點擊取消新手教學(滑鼠移動座標) 1.麻將 2.森林舞會
    new_mousemove_mahjong = 392,649
    new_mousemove_forest = 700,179

    #--------------------------------------------------------
    @classmethod
    def setUpClass(self):
        # Selenium
        # 取消網頁中的彈出視窗，避免妨礙網路爬蟲的執行
        options = Options()
        options.add_argument("--disable-notifications")
        # 引用webdriver
        self.chrome = webdriver.Chrome(self.driver_space, chrome_options=options)
        # 開啟要爬的網址(KKGAME_UAT後台)
        self.chrome.get(config.url)
        #self.chrome.maximize_window()
        
        # 取得網站的title
        title = self.chrome.title
        print("title :",title)
        print("版本 : ",version)
        time.sleep(3)

    @classmethod
    def tearDownClass(self):
        # 所有case跑完後就退出瀏覽器
        self.chrome.quit()

    #--------------------------------------------------------
    def test_01_login(self):
        '''登入'''
        # 應用find_element_by_id 來建立物件
        user = self.chrome.find_element("xpath","//body/div[@id='app']/div[1]/div[1]/section[1]/form[1]/div[1]/div[1]/div[1]/input[1]")
        password = self.chrome.find_element("xpath","//body/div[@id='app']/div[1]/div[1]/section[1]/form[1]/div[2]/div[1]/div[1]/input[1]")
        # 應用send_keys()來模擬使用者輸入的資料(KKGAME_UAT後台帳密)
        user.send_keys(config.user)
        password.send_keys(config.password)
        time.sleep(3)

        # 點擊登入
        login = self.chrome.find_element("xpath","//body/div[@id='app']/div[1]/div[1]/section[1]/form[1]/div[3]/div[1]/button[1]")
        login.click()
        time.sleep(3)

    def test_02_opendemo(self):
        '''點擊遊戲DEMO功能''' 
        gamedemo = self.chrome.find_element("xpath","//body/div[@id='app']/section[1]/section[1]/aside[1]/div[1]/div[1]/div[1]/ul[1]/a[2]/li[1]/div[1]")
        gamedemo.click()
        time.sleep(3)

    #--------------------------------------------------------
    def test_03_opengame(self):
        '''開啟真龍虎爭霸'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[23]/td[3]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_g26.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")

        '''真龍虎爭霸比對'''
        img1 = self.background_space + r'/background_g26.png'
        img2 = self.ori_space + r'/g26.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_g26.png',getimage)
            picdata=self.vs_space + r'/vs_g26.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_g26_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_g26_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_04_opengame(self):
        '''開啟魔法糖果'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[17]/td[3]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_g20.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''魔法糖果比對'''
        img1 = self.background_space + r'/background_g20.png'
        img2 = self.ori_space + r'/g20.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_g20.png',getimage)
            picdata=self.vs_space + r'/vs_g20.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_g20_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_g20_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_05_opengame(self):
        '''開啟福祿壽'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[26]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_fuluso.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''福祿壽比對'''
        img1 = self.background_space + r'/background_fuluso.png'
        img2 = self.ori_space + r'/fuluso.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_fuluso.png',getimage)
            picdata=self.vs_space + r'/vs_fuluso.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_fuluso_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_fuluso_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_06_opengame(self):
        '''開啟深海历险'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[3]/td[2]/div[1]/button[1]/span[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_theocean.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''深海历险比對'''
        img1 = self.background_space + r'/background_theocean.png'
        img2 = self.ori_space + r'/theocean.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_theocean.png',getimage)
            picdata=self.vs_space + r'/vs_theocean.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_theocean_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_theocean_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_07_opengame(self):
        '''開啟封神榜'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[6]/td[2]/div[1]/button[1]/span[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_Fengshen.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''封神榜比對'''
        img1 = self.background_space + r'/background_Fengshen.png'
        img2 = self.ori_space + r'/Fengshen.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_Fengshen.png',getimage)
            picdata=self.vs_space + r'/vs_Fengshen.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_Fengshen_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_Fengshen_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_08_opengame(self):
        '''開啟玛雅遗迹'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[7]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_Mayan.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")

        '''玛雅遗迹比對'''
        img1 = self.background_space + r'/background_Mayan.png'
        img2 = self.ori_space + r'/Mayan.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_Mayan.png',getimage)
            picdata=self.vs_space + r'/vs_Mayan.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_Mayan_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_Mayan_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_09_opengame(self):
        '''開啟埃及艳后'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[8]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_Cleopatra.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''埃及艳后比對'''
        img1 = self.background_space + r'/background_Cleopatra.png'
        img2 = self.ori_space + r'/Cleopatra.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_Cleopatra.png',getimage)
            picdata=self.vs_space + r'/vs_Cleopatra.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_Cleopatra_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_Cleopatra_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_10_opengame(self):
        '''開啟SuperStar'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[9]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_SuperStar.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''SuperStar比對'''
        img1 = self.background_space + r'/background_SuperStar.png'
        img2 = self.ori_space + r'/SuperStar.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_SuperStar.png',getimage)
            picdata=self.vs_space + r'/vs_SuperStar.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_SuperStar_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_SuperStar_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_11_opengame(self):
        '''開啟侏罗纪乐园'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[10]/td[2]/div[1]/button[1]/span[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_Jurassic.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''侏罗纪乐园比對'''
        img1 = self.background_space + r'/background_Jurassic.png'
        img2 = self.ori_space + r'/Jurassic.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_Jurassic.png',getimage)
            picdata=self.vs_space + r'/vs_Jurassic.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_Jurassic_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_Jurassic_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_12_opengame(self):
        '''開啟西游大闹天宫'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[11]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_theWest.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''西游大闹天宫比對'''
        img1 = self.background_space + r'/background_theWest.png'
        img2 = self.ori_space + r'/theWest.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_theWest.png',getimage)
            picdata=self.vs_space + r'/vs_theWest.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_theWest_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_theWest_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)
    
    #--------------------------------------------------------
    def test_13_opengame(self):
        '''開啟聚宝盆'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[12]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_treasure.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''聚宝盆比對'''
        img1 = self.background_space + r'/background_treasure.png'
        img2 = self.ori_space + r'/treasure.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_treasure.png',getimage)
            picdata=self.vs_space + r'/vs_treasure.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_treasure_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_treasure_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_14_opengame(self):
        '''開啟亚瑟王'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[13]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_KingArthur.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''亚瑟王比對'''
        img1 = self.background_space + r'/background_KingArthur.png'
        img2 = self.ori_space + r'/KingArthur.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_KingArthur.png',getimage)
            picdata=self.vs_space + r'/vs_KingArthur.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_KingArthur_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_KingArthur_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_15_opengame(self):
        '''開啟福虎'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[18]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_Fuhu.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''福虎比對'''
        img1 = self.background_space + r'/background_Fuhu.png'
        img2 = self.ori_space + r'/Fuhu.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_Fuhu.png',getimage)
            picdata=self.vs_space + r'/vs_Fuhu.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_Fuhu_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_Fuhu_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_16_opengame(self):
        '''開啟龙神'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[19]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_DragonGod.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''龙神比對'''
        img1 = self.background_space + r'/background_DragonGod.png'
        img2 = self.ori_space + r'/DragonGod.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_DragonGod.png',getimage)
            picdata=self.vs_space + r'/vs_DragonGod.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_DragonGod_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_DragonGod_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_17_opengame(self):
        '''開啟凤凰传奇'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[21]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_Phoenix.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''凤凰传奇比對'''
        img1 = self.background_space + r'/background_Phoenix.png'
        img2 = self.ori_space + r'/Phoenix.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_Phoenix.png',getimage)
            picdata=self.vs_space + r'/vs_Phoenix.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_Phoenix_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_Phoenix_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_18_opengame(self):
        '''開啟龙虎争霸'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[22]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_tiger.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''龙虎争霸比對'''
        img1 = self.background_space + r'/background_tiger.png'
        img2 = self.ori_space + r'/tiger.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_tiger.png',getimage)
            picdata=self.vs_space + r'/vs_tiger.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_tiger_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_tiger_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_19_opengame(self):
        '''開啟动物王国'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[24]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_animalkingdom.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''动物王国比對'''
        img1 = self.background_space + r'/background_animalkingdom.png'
        img2 = self.ori_space + r'/animalkingdom.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_animalkingdom.png',getimage)
            picdata=self.vs_space + r'/vs_animalkingdom.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_animalkingdom_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_animalkingdom_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_20_opengame(self):
        '''開啟森林舞会'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[25]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(10)
        pyautogui.moveTo(self.new_mousemove_forest)
        pyautogui.click()
        time.sleep(5)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_forestball.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''森林舞会比對'''
        img1 = self.background_space + r'/background_forestball.png'
        img2 = self.ori_space + r'/forestball.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_forestball.png',getimage)
            picdata=self.vs_space + r'/vs_forestball.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_forestball_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_forestball_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_21_opengame(self):
        '''開啟武圣传'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[27]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_WuSheng.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''武圣传比對'''
        img1 = self.background_space + r'/background_WuSheng.png'
        img2 = self.ori_space + r'/WuSheng.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_WuSheng.png',getimage)
            picdata=self.vs_space + r'/vs_WuSheng.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_WuSheng_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_WuSheng_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_22_opengame(self):
        '''開啟闪亮水果盘'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[28]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_shinyfruit.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''闪亮水果盘比對'''
        img1 = self.background_space + r'/background_shinyfruit.png'
        img2 = self.ori_space + r'/shinyfruit.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_shinyfruit.png',getimage)
            picdata=self.vs_space + r'/vs_shinyfruit.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_shinyfruit_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_shinyfruit_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_23_opengame(self):
        '''開啟燥起来'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[36]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_dryup.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''燥起来比對'''
        img1 = self.background_space + r'/background_dryup.png'
        img2 = self.ori_space + r'/dryup.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_dryup.png',getimage)
            picdata=self.vs_space + r'/vs_dryup.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_dryup_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_dryup_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_24_opengame(self):
        '''開啟印度之心'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[45]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_India.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''印度之心比對'''
        img1 = self.background_space + r'/background_India.png'
        img2 = self.ori_space + r'/India.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_India.png',getimage)
            picdata=self.vs_space + r'/vs_India.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_India_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_India_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_25_opengame(self):
        '''開啟抢庄牛牛'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[1]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_GrabZhuangNiuNiu.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''抢庄牛牛比對'''
        img1 = self.background_space + r'/background_GrabZhuangNiuNiu.png'
        img2 = self.ori_space + r'/GrabZhuangNiuNiu.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_GrabZhuangNiuNiu.png',getimage)
            picdata=self.vs_space + r'/vs_GrabZhuangNiuNiu.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_GrabZhuangNiuNiu_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_GrabZhuangNiuNiu_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_26_opengame(self):
        '''開啟通比牛牛'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[2]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_TumblrNiuNiu.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''通比牛牛比對'''
        img1 = self.background_space + r'/background_TumblrNiuNiu.png'
        img2 = self.ori_space + r'/TumblrNiuNiu.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_TumblrNiuNiu.png',getimage)
            picdata=self.vs_space + r'/vs_TumblrNiuNiu.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_TumblrNiuNiu_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_TumblrNiuNiu_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)
    #brent_yang_create
    #--------------------------------------------------------
    def test_27_opengame(self):
        '''開啟三公'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[4]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_Sangong.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''三公比對'''
        img1 = self.background_space + r'/background_Sangong.png'
        img2 = self.ori_space + r'/Sangong.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_Sangong.png',getimage)
            picdata=self.vs_space + r'/vs_Sangong.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_Sangong_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_Sangong_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_28_opengame(self):
        '''開啟正宗抢庄牛牛'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[29]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_AuthenticRobZhuangNiuNiu.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''正宗抢庄牛牛比對'''
        img1 = self.background_space + r'/background_AuthenticRobZhuangNiuNiu.png'
        img2 = self.ori_space + r'/AuthenticRobZhuangNiuNiu.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_AuthenticRobZhuangNiuNiu.png',getimage)
            picdata=self.vs_space + r'/vs_AuthenticRobZhuangNiuNiu.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_AuthenticRobZhuangNiuNiu_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_AuthenticRobZhuangNiuNiu_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_29_opengame(self):
        '''開啟正宗通比牛牛'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[30]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_AuthenticTongbiNiuNiu.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''正宗通比牛牛比對'''
        img1 = self.background_space + r'/background_AuthenticTongbiNiuNiu.png'
        img2 = self.ori_space + r'/AuthenticTongbiNiuNiu.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_AuthenticTongbiNiuNiu.png',getimage)
            picdata=self.vs_space + r'/vs_AuthenticTongbiNiuNiu.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_AuthenticTongbiNiuNiu_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_AuthenticTongbiNiuNiu_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)
    
    #--------------------------------------------------------
    def test_30_opengame(self):
        '''開啟正宗三公'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[31]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_AuthenticSanGong.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''正宗三公比對'''
        img1 = self.background_space + r'/background_AuthenticSanGong.png'
        img2 = self.ori_space + r'/AuthenticSanGong.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_AuthenticSanGong.png',getimage)
            picdata=self.vs_space + r'/vs_AuthenticSanGong.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_AuthenticSanGong_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_AuthenticSanGong_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_31_opengame(self):
        '''開啟大众麻将'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[5]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        pyautogui.moveTo(self.new_mousemove_mahjong)
        pyautogui.click()
        time.sleep(5)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_PopularMahjong.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''大众麻将比對'''
        img1 = self.background_space + r'/background_PopularMahjong.png'
        img2 = self.ori_space + r'/PopularMahjong.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_PopularMahjong.png',getimage)
            picdata=self.vs_space + r'/vs_PopularMahjong.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_PopularMahjong_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_PopularMahjong_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_32_opengame(self):
        '''開啟红中麻将'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[14]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        pyautogui.moveTo(self.new_mousemove_mahjong)
        pyautogui.click()
        time.sleep(5)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_RedChineseMahjong.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''红中麻将比對'''
        img1 = self.background_space + r'/background_RedChineseMahjong.png'
        img2 = self.ori_space + r'/RedChineseMahjong.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_RedChineseMahjong.png',getimage)
            picdata=self.vs_space + r'/vs_RedChineseMahjong.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_RedChineseMahjong_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_RedChineseMahjong_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_33_opengame(self):
        '''開啟血流成河'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[15]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        pyautogui.moveTo(self.new_mousemove_mahjong)
        pyautogui.click()
        time.sleep(5)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_riverofblood.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''血流成河比對'''
        img1 = self.background_space + r'/background_riverofblood.png'
        img2 = self.ori_space + r'/riverofblood.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_riverofblood.png',getimage)
            picdata=self.vs_space + r'/vs_riverofblood.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_riverofblood_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_riverofblood_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_34_opengame(self):
        '''開啟血战到底'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[16]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        pyautogui.moveTo(self.new_mousemove_mahjong)
        pyautogui.click()
        time.sleep(5)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_bloodybattle.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''血战到底比對'''
        img1 = self.background_space + r'/background_bloodybattle.png'
        img2 = self.ori_space + r'/bloodybattle.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_bloodybattle.png',getimage)
            picdata=self.vs_space + r'/vs_bloodybattle.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_bloodybattle_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_bloodybattle_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_35_opengame(self):
        '''開啟温州麻将'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[32]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        pyautogui.moveTo(self.new_mousemove_mahjong)
        pyautogui.click()
        time.sleep(5)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_WenzhouMahjong.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''温州麻将比對'''
        img1 = self.background_space + r'/background_WenzhouMahjong.png'
        img2 = self.ori_space + r'/WenzhouMahjong.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_WenzhouMahjong.png',getimage)
            picdata=self.vs_space + r'/vs_WenzhouMahjong.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_WenzhouMahjong_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_WenzhouMahjong_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_36_opengame(self):
        '''開啟上海麻将'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[33]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        pyautogui.moveTo(self.new_mousemove_mahjong)
        pyautogui.click()
        time.sleep(5)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_ShanghaiMahjong.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''上海麻将比對'''
        img1 = self.background_space + r'/background_ShanghaiMahjong.png'
        img2 = self.ori_space + r'/ShanghaiMahjong.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_ShanghaiMahjong.png',getimage)
            picdata=self.vs_space + r'/vs_ShanghaiMahjong.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_ShanghaiMahjong_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_ShanghaiMahjong_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_37_opengame(self):
        '''開啟麻将来了'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[35]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_Mahjongcoming.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''麻将来了比對'''
        img1 = self.background_space + r'/background_Mahjongcoming.png'
        img2 = self.ori_space + r'/Mahjongcoming.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_Mahjongcoming.png',getimage)
            picdata=self.vs_space + r'/vs_Mahjongcoming.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_Mahjongcoming_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_Mahjongcoming_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_38_opengame(self):
        '''開啟富贵捕鱼'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[46]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_richfishing.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''富贵捕鱼比對'''
        img1 = self.background_space + r'/background_richfishing.png'
        img2 = self.ori_space + r'/richfishing.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_richfishing.png',getimage)
            picdata=self.vs_space + r'/vs_richfishing.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_richfishing_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_richfishing_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_39_opengame(self):
        '''開啟猜硬币'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[47]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_coin.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''猜硬币比對'''
        img1 = self.background_space + r'/background_coin.png'
        img2 = self.ori_space + r'/coin.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_coin.png',getimage)
            picdata=self.vs_space + r'/vs_coin.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_coin_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_coin_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_40_opengame(self):
        '''開啟骰子游戏'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[48]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_dicegame.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''骰子游戏比對'''
        img1 = self.background_space + r'/background_dicegame.png'
        img2 = self.ori_space + r'/dicegame.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_dicegame.png',getimage)
            picdata=self.vs_space + r'/vs_dicegame.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_dicegame_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_dicegame_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_41_opengame(self):
        '''開啟百家乐'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[34]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_Baccarat.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''百家乐比對'''
        img1 = self.background_space + r'/background_Baccarat.png'
        img2 = self.ori_space + r'/Baccarat.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_Baccarat.png',getimage)
            picdata=self.vs_space + r'/vs_Baccarat.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_Baccarat_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_Baccarat_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_42_opengame(self):
        '''開啟猛龙传说'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[20]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_dragonlee.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''猛龙传说比對'''
        img1 = self.background_space + r'/background_dragonlee.png'
        img2 = self.ori_space + r'/dragonlee.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_dragonlee.png',getimage)
            picdata=self.vs_space + r'/vs_dragonlee.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_dragonlee_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_dragonlee_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_43_opengame(self):
        '''開啟十胜节'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[49]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_Dussehra.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''十胜节比對'''
        img1 = self.background_space + r'/background_Dussehra.png'
        img2 = self.ori_space + r'/Dussehra.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_Dussehra.png',getimage)
            picdata=self.vs_space + r'/vs_Dussehra.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_Dussehra_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_Dussehra_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_44_opengame(self):
        '''開啟龙王'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[38]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_dragonking.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''龙王比對'''
        img1 = self.background_space + r'/background_dragonking.png'
        img2 = self.ori_space + r'/dragonking.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_dragonking.png',getimage)
            picdata=self.vs_space + r'/vs_dragonking.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_dragonking_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_dragonking_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_45_opengame(self):
        '''開啟红黑梅方'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[40]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_redblack.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''红黑梅方比對'''
        img1 = self.background_space + r'/background_redblack.png'
        img2 = self.ori_space + r'/redblack.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_redblack.png',getimage)
            picdata=self.vs_space + r'/vs_redblack.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_redblack_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_redblack_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)
  
    #--------------------------------------------------------
    def test_46_opengame(self):
        '''開啟射龙门'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[39]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_shootingdragon.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''射龙门比對'''
        img1 = self.background_space + r'/background_shootingdragon.png'
        img2 = self.ori_space + r'/shootingdragon.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_shootingdragon.png',getimage)
            picdata=self.vs_space + r'/vs_shootingdragon.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_shootingdragon_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_shootingdragon_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_47_opengame(self):
        '''開啟连环夺宝'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[41]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_serialtreasurehunt.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''连环夺宝比對'''
        img1 = self.background_space + r'/background_serialtreasurehunt.png'
        img2 = self.ori_space + r'/serialtreasurehunt.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_serialtreasurehunt.png',getimage)
            picdata=self.vs_space + r'/vs_serialtreasurehunt.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_serialtreasurehunt_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_serialtreasurehunt_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_48_opengame(self):
        '''開啟招财喵喵'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[52]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_LuckyCat.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''招财喵喵'''
        img1 = self.background_space + r'/background_LuckyCat.png'
        img2 = self.ori_space + r'/LuckyCat.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_LuckyCat.png',getimage)
            picdata=self.vs_space + r'/vs_LuckyCat.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_LuckyCat_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_LuckyCat_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_49_opengame(self):
        '''開啟斗三公'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[37]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_DouSanGong.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''斗三公'''
        img1 = self.background_space + r'/background_DouSanGong.png'
        img2 = self.ori_space + r'/DouSanGong.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_DouSanGong.png',getimage)
            picdata=self.vs_space + r'/vs_DouSanGong.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_DouSanGong_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_DouSanGong_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_50_opengame(self):
        '''開啟滿天星'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[42]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_Gypsophila.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''滿天星'''
        img1 = self.background_space + r'/background_Gypsophila.png'
        img2 = self.ori_space + r'/Gypsophila.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_Gypsophila.png',getimage)
            picdata=self.vs_space + r'/vs_Gypsophila.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_Gypsophila_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_Gypsophila_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_51_opengame(self):
        '''開啟全民21点'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[44]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_point21.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''全民21点'''
        img1 = self.background_space + r'/background_point21.png'
        img2 = self.ori_space + r'/point21.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_point21.png',getimage)
            picdata=self.vs_space + r'/vs_point21.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_point21_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_point21_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_52_opengame(self):
        '''開啟叶猴'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[51]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_leafmonkey.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''叶猴'''
        img1 = self.background_space + r'/background_leafmonkey.png'
        img2 = self.ori_space + r'/leafmonkey.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_leafmonkey.png',getimage)
            picdata=self.vs_space + r'/vs_leafmonkey.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_leafmonkey_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_leafmonkey_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_53_opengame(self):
        '''開啟宝象'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[43]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_elephant.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''宝象'''
        img1 = self.background_space + r'/background_elephant.png'
        img2 = self.ori_space + r'/elephant.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_elephant.png',getimage)
            picdata=self.vs_space + r'/vs_elephant.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_elephant_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_elephant_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_54_opengame(self):
        '''開啟安达·巴哈'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[50]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_andabaja.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''安达·巴哈'''
        img1 = self.background_space + r'/background_andabaja.png'
        img2 = self.ori_space + r'/andabaja.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_andabaja.png',getimage)
            picdata=self.vs_space + r'/vs_andabaja.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_andabaja_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_andabaja_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)

    #--------------------------------------------------------
    def test_55_opengame(self):
        '''開啟鱼虾蟹开了'''
        dragon = self.chrome.find_element("xpath","//body[1]/div[1]/section[1]/section[1]/main[1]/main[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/table[1]/tbody[1]/tr[50]/td[2]/div[1]/button[1]")
        dragon.click()
        time.sleep(self.open_sleep)
        game_title = self.chrome.title
        print("<br>------------------------")
        print("<br>game_title :",game_title)
        print("<br>------------------------")

        '''擷取主畫面'''
        save_path = os.path.join(os.path.expanduser('~'), self.background_space, "background_Fishandshrimpandcrab.png")
        self.chrome.find_element("xpath","//div[@id='Cocos2dGameContainer']//canvas[1]").screenshot(save_path)
        time.sleep(self.pic_sleep)
        print("<br>------------------------")
        print("<br>擷取主畫面 :成功")
        print("<br>------------------------")
    
        '''鱼虾蟹开了'''
        img1 = self.background_space + r'/background_Fishandshrimpandcrab.png'
        img2 = self.ori_space + r'/Fishandshrimpandcrab.png'
        pic = pictest.get_image_element_point(img1,img2)
        getimage = pictest.get_vsimage(img1,img2)

        if pic >= self.feature:
            plt.imsave(self.vs_space + '/vs_Fishandshrimpandcrab.png',getimage)
            picdata=self.vs_space + r'/vs_Fishandshrimpandcrab.png'
            print("<span class = red-bg1>圖像比對 :成功，有符合的圖像</span>")
            print("<img src='" + picdata + "'width=600 />")
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
            plt.imsave(self.vs_space + '/vs_Fishandshrimpandcrab_fail.png',getimage)
            picdata_fail=self.vs_space + r'/vs_Fishandshrimpandcrab_fail.png'
            self.chrome.back()
            class DemoException(Exception):
                def __init__(self, message):
                    super().__init__(message)
            message = "<span class = red-bg1>遊戲比對 :失敗，實際畫面與原圖有差異</span>"
            print("<img src='" + picdata_fail + "'width=600 />")
            raise DemoException(message)
        time.sleep(15)
 
 
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
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(Test))
    result = BeautifulReport(testunit)
    result.report(
        filename = f"kkgame_report_{config.DATE}",
        description = f"KKGAME_測試報告({config.DATE})", 
        log_path=config.REPORT_GEN_DIR
    )
# 啟動自動化指令，在終端機輸入: & C:/Users/你的使用者帳號/AppData/Local/Programs/Python/Python39/python.exe d:/auto_test/firstCase.py