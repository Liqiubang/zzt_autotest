# conftest.py（核心配置文件）
import pytest
from webdriver_helper import get_webdriver
import logging
logger = logging.getLogger(__name__)
from selenium.webdriver.support.wait import WebDriverWait

@pytest.fixture(autouse=False, scope="session")
def fixture_browser():
    """全局浏览器管理fixture"""
    driver = get_webdriver('chrome')
    driver.maximize_window()
    logger.info("夹具初始化完成，浏览器启动成功")
    yield driver
    driver.quit()