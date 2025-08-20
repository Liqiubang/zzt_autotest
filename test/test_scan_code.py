import json
import time
import pytest
from webdriver_helper import get_webdriver

# def save_cookies_manually():
#     """首次手动扫码登录并保存Cookie"""
#     driver = get_webdriver('chrome')
#     driver.maximize_window()
#     driver.get("http://smart-operation-sit.cm253.com/login")
#     input("请扫码登录后按回车保存Cookie...")
#
#     cookies = driver.get_cookies()
#     with open("cookies.json", "w") as f:
#         json.dump(cookies, f)
#     driver.quit()
#
# @pytest.fixture(scope="session")
# def driver_with_cookies():
#     """pytest fixture加载已保存的Cookie"""
#     driver = get_webdriver('chrome')
#     driver.maximize_window()
#     driver.get("http://smart-operation-sit.cm253.com")  # 先访问域名写入Cookie
#
#     try:
#         with open("cookies.json", "r") as f:
#             cookies = json.load(f)
#             for cookie in cookies:
#                 if "expiry" in cookie:  # 处理过期时间字段
#                     cookie["expiry"] = int(cookie["expiry"])
#                 driver.add_cookie(cookie)
#         driver.refresh()
#     except FileNotFoundError:
#         save_cookies_manually()  # 首次运行自动触发保存流程
#
#     yield driver
#     driver.quit()
#
# def test_protected_page(driver_with_cookies):
#     """测试需要登录态的页面"""
#     driver_with_cookies.get("http://smart-operation-sit.cm253.com/home")
#     time.sleep(5)
#     assert "智能运营平台" in driver_with_cookies.title


def test_protected_page(fixture_browser):
    fixture_browser.get("https://smart-operation.new253.com/login")
    input("请扫码登录后按回车继续。。。")
    fixture_browser.get("https://smart-operation.new253.com/child-risk/review/text-tem")
    time.sleep(5)
    assert "智能运营平台-风控中心" in fixture_browser.title
