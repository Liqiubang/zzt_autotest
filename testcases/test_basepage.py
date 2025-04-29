import logging
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import alert_is_present
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


logger = logging.getLogger(__name__)

class TestBasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_element(self, xpath):
        logger.info(f"正在定位元素：{xpath=}")
        allure.attach(self.driver.get_screenshot_as_png(), name="定位元素截图",
                      attachment_type=allure.attachment_type.PNG)  # 定位前截图
        el = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))  # 元素可见时返回元素对象 自动等待元素出现 参数是元组，所以要多加一组小括号
        logger.info(f"元素定位成功：tag_name{el.tag_name}")
        return el

    def __getattr__(self, item):  # 访问不存在的属性时触发  item=username
        if not item.startswith('_loc_'):  # 避免递归调用
            key = f"_loc_{item}"  # 动态生成属性名 key=_loc_username
            xpath = getattr(self, key)  # 获取_loc_username的属性值  与__getattr__作用不一样
            # pdb.set_trace()
            if xpath is not None:
                return self.get_element(xpath)
        raise AttributeError(f"属性 '{item}' 不存在")

    def alert_ok(self):
        logger.info("正在处理弹窗")
        alert = self.driver.wait.until(alert_is_present)
        alert.accept()
        logger.info("弹窗处理完成")

"""Page类作为基类被其他页面类继承，子类在初始化时会调用父类的构造函数，传递driver参数"""
class TestLoginSuccessPage(TestBasePage):
    def __init__(self, driver):
        super().__init__(driver)  # 调用基类构造函数
        self.username = "//input[@id='username']"
        self.password = "//input[@id='password']"
        self.login_btn = "//*[@id='clApp']/div/div[1]/div[2]/div[2]/div/div/form/div[4]/div/div/div/button/span[1]"

    def login(self, username, password):
        logger.info("准备登录")
        self.get_element(self.username).send_keys(username)
        self.get_element(self.password).send_keys(password)
        self.get_element(self.login_btn).click()
        logger.info("登录成功")
        allure.attach(self.driver.get_screenshot_as_png(), "登录成功截图", allure.attachment_type.PNG)  # 交互后截图