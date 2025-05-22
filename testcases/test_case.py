import time
import pytest
from testcases.test_basepage import *
import logging
from utils.database_ck import query_from_ck
logger = logging.getLogger(__name__)

"""pytest 会通过 ‌参数名匹配‌ 自动查找conftest.py 并注入已注册的夹具（fixture_browser）
并将其返回值（即 driver 对象）传递给测试函数"""


@pytest.fixture(scope="session")
def test_login_success(fixture_browser, env_config):
    logger.info("浏览器已启动")
    login_url = f"{env_config['login_url']}"
    fixture_browser.get(login_url)
    page = TestLoginSuccessPage(fixture_browser)
    username = f"{env_config['username']}"
    password = f"{env_config['password']}"
    page.login(username, password)
    control_url = f"{env_config['control_url']}"
    assert fixture_browser.current_url == control_url
    logger.info("登录成功")
    return fixture_browser


@pytest.mark.smoke
@pytest.mark.parametrize("phone", [15274438093, 13203173318, 19074910586])
# @pytest.mark.parametrize("phone", [15274438093])
def test_send_constant_sms(test_login_success, env_config, phone):
    page = TestSendConstantSmsPage(test_login_success)
    page.sendConstantSms(env_config, phone)
    login_url = f"{env_config['login_url']}"
    if login_url.__eq__("https://cloudsit.cm253.com/control/login"):
        time.sleep(60)  # 等待入库
        try:
            ckResult = query_from_ck()
            content = str(ckResult[0][36])
            report = str(ckResult[0][40])
        except IndexError:
            print("索引异常，请检查数据库中数据！")
        assert content.__eq__("【创蓝云智】测试 www.baidu.com 测试拒收请回复R") and report.__eq__("DELIVRD")
    else:
        assert page.get_element(page.sendRecord).text == "【上海木南测试】测试 www.baidu.com 短信拒收请回复R"


@pytest.mark.smoke
def test_send_variable_sms(test_login_success, env_config):
    page = TestSendVariableSmsPage(test_login_success)
    page.sendVariableSms(env_config)
    login_url = f"{env_config['login_url']}"
    if login_url.__eq__("https://cloudsit.cm253.com/control/login"):
        time.sleep(60)  # 等待入库
        try:
            ckResult = query_from_ck()
            content = str(ckResult[0][36])
            report = str(ckResult[0][40])
        except IndexError:
            print("索引异常，请检查数据库中数据！")
        assert content.__eq__("【创蓝云智】白模版测试(测试)小红红拒收请回复R") and report.__eq__("DELIVRD")
    else:
        assert page.get_element(page.sendRecord).text == "【上海木南测试】白模版测试「测试」小红红拒收请回复R"


if __name__ == '__main__':
    test_send_constant_sms()
