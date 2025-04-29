from testcases.test_basepage import TestLoginSuccessPage
import logging

logger = logging.getLogger(__name__)

"""pytest 会通过 ‌参数名匹配‌ 自动查找conftest.py 并注入已注册的夹具（fixture_browser）
并将其返回值（即 driver 对象）传递给测试函数"""
def test_login_success(fixture_browser):
    logger.info("浏览器已启动")
    fixture_browser.get("https://cloudsit.cm253.com/control/login")
    page = TestLoginSuccessPage(fixture_browser)
    page.login("16673532843", "Li94122334@")
    msg = "登录成功"
    assert msg == "登录成功"
    logger.info("登录成功")

if __name__ == '__main__':
    test_login_success()
