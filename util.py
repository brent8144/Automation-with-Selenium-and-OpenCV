# Standard Library Modules
import json

from http import HTTPStatus

# Third-Party Library Modules
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By

# Local Application/Project-Specific Modules
import config


def update_slot_cheat_table(domain: str, data: dict):
    """
    透過 API 對配牌器請求更新指定玩家配牌結果

    Args:
     - domain (str): 配牌器 domain
     - data (dict): 配牌封包, 具體結構請參考 README 說明

    Returns:
     - str: 資料庫更新紀錄, 若為空字串表示更新失敗
    """
    
    url = f"{domain}/api/common/document/"
    headers = {
        'Content-type': 'application/json;charset=UTF-8'
    }
    
    resp = requests.put(url, data=json.dumps(data), headers=headers)
    
    return resp.json().get("_rev") if resp.status_code == HTTPStatus.OK else ""


def waiting_cocos_loading(driver: webdriver.Chrome) -> bool:
    """
    判斷特定 div 出現後才表示載入完成

    Args:
     - driver (selenium.webdriver.Chrome): Google Chrome Driver

    Returns:
     - bool: 是否已經載入完成
    """
    driver.find_element(By.ID, "colorBlock")
    return True


def get_kkgame_admin_access_token(domain: str, username: str, password: str) -> str:
    """
    透過 API 對 KKGame 管理後台請求取得 access token

    Args:
     - domain (str): KKGame 管理後台 domain
     - username (str): 用戶帳號
     - password (str): 用戶密碼

    Returns:
     - str: access token, 若為空字串表示取得失敗
    """

    url = f"{domain}/api/v2/auth/login"
    data = {
        "username": username,
        "password": password
    }
    headers = {
        'Content-type': 'application/json;charset=UTF-8'
    }

    resp = requests.post(url, data=json.dumps(data), headers=headers)

    # 當狀態碼為 200 時就返回 access token, 否則為空
    return resp.json().get("token") if resp.status_code == HTTPStatus.OK else ""


def get_kkgame_game_url(domain: str, token: str, gameid: str, ecsiteid: str, lang: str) -> str:
    """
    透過 API 對 KKGame 管理後台請求取得指定遊戲的遊戲連結

    Args:
     - domain (str): KKGame 管理後台 domain
     - token (str): access token
     - gameid (str): 遊戲識別碼
     - ecsiteid (str): 渠道識別碼
     - lang (str): 語系代碼

    Returns:
     - str: 遊戲連結
    """

    url = f"{domain}/api/v2/demo/games/{gameid}/{ecsiteid}/launch?lang={lang}"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    resp = requests.get(url, headers=headers)

    # 當狀態碼為 200 時就返回遊戲連結, 否則為空
    return resp.json().get("url") if resp.status_code == HTTPStatus.OK else ""


if __name__ == "__main__":
    token = get_kkgame_admin_access_token(
        config.KK_ADMIN_URL,
        config.KK_ADMIN_USER,
        config.KK_ADMIN_PASSWORD,
    )

    url = get_kkgame_game_url(
        config.KK_ADMIN_URL,
        token,
        "7",
        "1",
        "zh-cn",
    )

    print(url)
