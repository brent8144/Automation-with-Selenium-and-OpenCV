![KKGAME_Comparison.py]
![KKGAME_LV_Comparison.py]
![main.py]
## KKGAME_Comparison
## KKGAME_LV_Comparison
## main
#brent_yang
0. 需建立圖片及報告存放的資料夾(KKGAME_PIC、KKGAME_PIC_BACKGROUND、KKGAME_PIC_VS、KKGAME_REPORT)

1. 需擷取所有遊戲原圖並放置在「KKGAME_PIC」資料夾，已先提供目前所有遊戲截圖並放置在該資料夾(20221109)

2. 修改圖片存放路徑 & driver位置 & 報告存放路徑 (main.py)
#測試報告位置
basedir = "C:/Users/brent_yang/Desktop/Selenium/KKGAME_REPORT"
#chrome driver位置
driver_space = r'C:\Users\brent_yang\Desktop\Selenium\chromedriver'
#原圖存放位置
ori_space = "C:/Users/brent_yang/Desktop/Selenium/KKGAME_PIC"
#擷取圖片存放位置
background_space = "C:/Users/brent_yang/Desktop/Selenium/KKGAME_PIC_BACKGROUND"
#比對圖片存放位置
vs_space = "C:/Users/brent_yang/Desktop/Selenium/KKGAME_PIC_VS"

3. 修改KK後台/LV平台的帳號密碼
    3-1.登入KK後台(uat) 設定帳號&密碼(user、password)
        def test_01_login(self):
            '''登入'''
            # 應用find_element_by_id 來建立物件
            user = self.chrome.find_element_by_xpath("//body/div[@id='app']/div[1]/div[1]/section[1]/form[1]/div[1]/div[1]/div[1]/input[1]")
            password = self.chrome.find_element_by_xpath("//body/div[@id='app']/div[1]/div[1]/section[1]/form[1]/div[2]/div[1]/div[1]/input[1]")

            # 應用send_keys()來模擬使用者輸入的資料(KKGAME_UAT後台帳密)
    -->     user.send_keys('後台帳號')    
    -->     password.send_keys('後台密碼')

    3-2.登入LV平台(uat) 設定帳號&密碼&驗證碼(user、password、key)
        def test_01_login(self):     
            '''關閉訊息'''
            pyautogui.moveTo(1399,325)
            pyautogui.click()
            time.sleep(3)

            '''登入'''
            # 應用find_element_by_id 來建立物件
            user = self.chrome.find_element_by_xpath("//input[@id='nzc-header-account']")
            password = self.chrome.find_element_by_xpath("//input[@id='nzc-header-password']")
            key = self.chrome.find_element_by_xpath("//input[@id='nzc-header-captcha']")

            # 應用send_keys()來模擬使用者輸入的資料(LV平台帳密)
    -->     user.send_keys('帳號')
    -->     password.send_keys('密碼')
    -->     key.send_keys('1')
            time.sleep(3)

4. 有使用html的語法來調整BeautifulReport部分文字顏色，需至BeautifulReport的Lib新增色碼參數
    Lib位置如下:
    C:\Users\XXXX\AppData\Local\Programs\Python\Python39\Lib\site-packages\BeautifulReport\template

    新增色碼(開啟template，使用Ctrl+f 搜尋blue，加在.blue-bg{}下面):
    .blue-bg1 {
        background-color: #0000CC;
        color: #fff
    }
    .yellow-bg1 {
        background-color: #FFFF00;
    }
    .red-bg1 {
        background-color: #FFFF00;
        color: #ED5565
    }

5. 如執行時會閃退，代表chromedriver與chrome版本不符，需至chrpme官網下載新版本的chromedriver。