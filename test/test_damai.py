from selenium.webdriver.common.by import By
from selenium import webdriver
import time


def test_damai_login():
    driver = webdriver.Chrome()
    driver.maximize_window()

    login_phone = "//input[@aria-label='请输入手机号或邮箱']"
    login_password = "//input[@aria-label='请输入登录密码']"
    login_btn = "//button[text()='登录']"


    driver.get("https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F")
    driver.switch_to.frame("alibaba-login-box")
    driver.find_element(By.XPATH, login_phone).send_keys("15274438093")
    driver.find_element(By.XPATH, login_password).send_keys("Li94122334@")
    driver.find_element(By.XPATH, login_btn).click()
    time.sleep(5)


if __name__ == '__main__':
    test_damai_login()
