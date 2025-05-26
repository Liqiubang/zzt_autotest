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
    username = f"{env_config['username']}"
    password = f"{env_config['password']}"
    control_url = f"{env_config['control_url']}"
    fixture_browser.get(login_url)
    page = TestLoginSuccessPage(fixture_browser)
    page.login(username, password)
    assert fixture_browser.current_url == control_url
    logger.info("登录成功")
    return fixture_browser


@pytest.mark.smoke
# @pytest.mark.parametrize("phone", [15274438093, 13203173318, 19074910586])
@pytest.mark.parametrize("phone", [15274438093])
def test_send_constant_sms(test_login_success, env_config, phone):
    page = TestSendConstantSmsPage(test_login_success)
    page.sendConstantSms(env_config, phone)
    login_url = f"{env_config['login_url']}"
    assert_constant_template = f"{env_config['assert_constant_template']}"
    assert_report = f"{env_config['assert_report']}"
    if login_url.__eq__("https://cloudsit.cm253.com/control/login"):
        time.sleep(60)  # 等待入库
        content = ""
        report = ""
        try:
            ckResult = query_from_ck()
            content = str(ckResult[0][36])
            report = str(ckResult[0][40])
        except IndexError:
            print("索引异常，请检查数据库中数据！")
        assert content == assert_constant_template and report == assert_report
        logger.info(
            f"断言 实际短信内容:{content} 断言内容:{assert_constant_template}\n 实际短信状态:{report} 断言状态:{assert_report}")
    else:
        time.sleep(10)  # 等待入库
        assert page.get_element(page.sendRecord).text == assert_constant_template
        logger.info(
            f"断言 实际短信内容:{page.get_element(page.sendRecord).text} 断言内容:{assert_constant_template}\n ")


@pytest.mark.smoke
def test_send_variable_sms(test_login_success, env_config):
    page = TestSendVariableSmsPage(test_login_success)
    page.sendVariableSms(env_config)
    login_url = f"{env_config['login_url']}"
    assert_variable_template = f"{env_config['assert_variable_template']}"
    assert_report = f"{env_config['assert_report']}"
    if login_url.__eq__("https://cloudsit.cm253.com/control/login"):
        time.sleep(60)  # 等待入库
        content = ""
        report = ""
        try:
            ckResult = query_from_ck()
            content = str(ckResult[0][36])
            report = str(ckResult[0][40])
        except IndexError:
            print("索引异常，请检查数据库中数据！")
        assert content == assert_variable_template and report == assert_report
        logger.info(
            f"断言 实际短信内容:{content} 断言内容:{assert_variable_template}\n 实际短信状态:{report} 断言状态:{assert_report}")
    else:
        time.sleep(10)  # 等待入库
        assert page.get_element(page.sendRecord).text == assert_variable_template
        logger.info(
            f"断言 实际短信内容:{page.get_element(page.sendRecord).text} 断言内容:{assert_variable_template}\n ")


if __name__ == '__main__':
    test_send_constant_sms()
