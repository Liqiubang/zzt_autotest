import os
import pytest
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_helper import get_webdriver
import logging
logger = logging.getLogger(__name__)
import yaml
options = Options()
# options.add_argument("--headless")  # Chrome 112+ 推荐语法
# options.add_argument("--disable-extensions")  # 禁用扩展
# options.add_argument("--disable-gpu")  # 关闭 GPU 加速
# options.add_argument("--no-sandbox")  # 关闭沙箱模式
# options.add_experimental_option("detach", True)  # 防止会话结束后自动关闭，保持浏览器实例复用，减少重复初始化
# options.add_argument('--disable-device-discovery-notifications')
# options.add_argument('--disable-usb-device-discovery')

@pytest.fixture(autouse=False, scope="session")
def fixture_browser():
    """全局浏览器管理fixture"""
    # driver = get_webdriver('chrome', options=options)
    driver = webdriver.Chrome()
    driver.maximize_window()
    logger.info("夹具初始化完成，浏览器启动成功")
    yield driver
    driver.quit()


def load_config():
    with open('C:\\Users\\15274\\PycharmProjects\\zzt_autotest\\config\\config.yml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def env_config():
    # env = os.getenv("sit", "sit")
    env = os.getenv("prod", "prod")
    config = load_config()
    return config["environments"][env]
