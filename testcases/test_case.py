import time

import pytest

from testcases.test_basepage import *
import logging
logger = logging.getLogger(__name__)

"""pytest 会通过 ‌参数名匹配‌ 自动查找conftest.py 并注入已注册的夹具（fixture_browser）
并将其返回值（即 driver 对象）传递给测试函数"""
@pytest.fixture(scope="session")
def test_login_success(fixture_browser):
    logger.info("浏览器已启动")
    fixture_browser.get("https://cloudsit.cm253.com/control/login")
    page = TestLoginSuccessPage(fixture_browser)
    page.login("16673532843", "Li94122334@")
    assert fixture_browser.current_url == "https://cloudsit.cm253.com/control/home"
    logger.info("登录成功")
    return fixture_browser

@pytest.mark.smoke
def test_send_sms(test_login_success):
    page = TestSendSmsPage(test_login_success)
    page.sendSms()
    time.sleep(10) #等待提示加载完成
    assert page.get_element(page.result).text == "检测完成，未发现异常！"

if __name__ == '__main__':
    test_send_sms()
