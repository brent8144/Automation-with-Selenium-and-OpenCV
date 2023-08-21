# Standard Library Modules
import os
import unittest

# Third-Party Library Modules
from BeautifulReport import BeautifulReport

# Local Application/Project-Specific Modules
import config

from GAME.g4_tester import G4Tester
from GAME.g7_tester import G7Tester
from GAME.g8_tester import G8Tester
from GAME.g9_tester import G9Tester
from GAME.g10_tester import G10Tester
from GAME.g11_tester import G11Tester
from GAME.g13_tester import G13Tester
from GAME.g14_tester import G14Tester
from GAME.g15_tester import G15Tester
from GAME.g20_tester import G20Tester
from GAME.g21_tester import G21Tester
from GAME.g22_tester import G22Tester
from GAME.g23_tester import G23Tester 
from GAME.g24_tester import G24Tester 
from GAME.g25_tester import G25Tester
from GAME.g26_tester import G26Tester
from GAME.g27_tester import G27Tester
from GAME.g31_tester import G31Tester
from GAME.g32_tester import G32Tester
from GAME.g33_tester import G33Tester #少1圖標
from GAME.g42_tester import G42Tester 
from GAME.g43_tester import G43Tester 
from GAME.g45_tester import G45Tester 
# from GAME.g48_tester import G48Tester #連環奪寶
from GAME.g50_tester import G50Tester 
from GAME.g53_tester import G53Tester
# from GAME.g56_tester import G56Tester #寶象
from GAME.g57_tester import G57Tester 
from GAME.g60_tester import G60Tester
from GAME.g64_tester import G64Tester 
from GAME.g139_tester import G139Tester 


if __name__ == '__main__':
    # 檢查所需資料夾是否存在
    if not os.path.exists(config.GROUND_TRUTU_DIR):
        os.mkdir(config.GROUND_TRUTU_DIR)
    if not os.path.exists(config.REPORT_ROOT_DIR):
        os.mkdir(config.REPORT_ROOT_DIR)

    # 建立這次測試的報告路徑
    os.mkdir(config.REPORT_GEN_DIR)

    print("--開始執行KKgame regression--")

    # 載入用例
    testunit = unittest.TestSuite()
    
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G4Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G7Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G8Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G9Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G10Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G11Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G13Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G14Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G15Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G20Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G21Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G22Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G23Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G24Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G25Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G26Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G27Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G31Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G32Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G33Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G42Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G43Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G45Tester))
    # #testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G48Tester)) #連環奪寶
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G50Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G53Tester))
    # #testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G56Tester)) #寶象
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G57Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G60Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G64Tester))
    testunit.addTests(unittest.TestLoader().loadTestsFromTestCase(G139Tester))

    # 輸出結果報告
    BeautifulReport(testunit).report(
        filename = f"kkgame_report_{config.DATE}", 
        description = f"KKGAME_測試報告({config.DATE})", 
        log_path = config.REPORT_GEN_DIR
    )
