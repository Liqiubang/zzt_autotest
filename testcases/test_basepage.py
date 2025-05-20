import random
import re  # 正则表达式匹配库
import time  # 事件库，用于硬性等待
import urllib  # 网络访问
import cv2  # opencv库
import logging
import allure
import document
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import alert_is_present
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains  # 动作类

from conftest import env_config

logger = logging.getLogger(__name__)


class TestBasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def get_element(self, xpath):
        logger.info(f"正在定位元素：{xpath=}")
        allure.attach(self.driver.get_screenshot_as_png(), name="定位元素截图",
                      attachment_type=allure.attachment_type.PNG)  # 定位前截图
        el = self.wait.until(
            # EC.presence_of_element_located((By.XPATH, xpath))) # 快速判断元素加载完成（如页面跳转后）
            # EC.visibility_of_element_located((By.XPATH, xpath)))  # 元素可见时返回元素对象,自动等待元素出现,参数是元组
            EC.element_to_be_clickable((By.XPATH, xpath)))  # 元素不仅需要可见，还需满足可交互条件
        logger.info(f"元素定位成功：tag_name{el.tag_name}")
        return el

    # def __getattr__(self, item):  # 访问不存在的属性时触发  item=username
    #     if not item.startswith('_loc_'):  # 避免递归调用
    #         key = f"_loc_{item}"  # 动态生成属性名 key=_loc_username
    #         xpath = getattr(self, key)  # 获取_loc_username的属性值  与__getattr__作用不一样
    #         # pdb.set_trace()
    #         if xpath is not None:
    #             return self.get_element(xpath)
    #     raise AttributeError(f"属性 '{item}' 不存在")

    def alert_ok(self):
        logger.info("正在处理弹窗")
        alert = self.driver.wait.until(alert_is_present)
        alert.accept()
        logger.info("弹窗处理完成")


# Page类作为基类被其他页面类继承，子类在初始化时会调用父类的构造函数，传递driver参数
# 登录成功
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
        time.sleep(3)

        # 解决登录时的滑块验证问题
        bigImage = self.driver.find_element(By.XPATH,
                                            "//div[@class='tencent-captcha-dy__verify-bg-img tencent-captcha-dy__unselectable']")
        s = bigImage.get_attribute("style")  # 获取图片的style属性
        # 设置能匹配出图片路径的正则表达式
        p = 'background-image: url\(\"(.*?)\"\);'
        # 进行正则表达式匹配，找出匹配的字符串并截取出来
        bigImageSrc = re.findall(p, s, re.S)[0]  # re.S表示点号匹配任意字符，包括换行符
        print("滑块验证图片下载路径:", bigImageSrc)
        # 下载图片至本地
        urllib.request.urlretrieve(bigImageSrc, './testcases/old.png')
        # 计算缺口图像的x轴位置
        dis = self.get_pos('./testcases/old.png')
        # 获取小滑块元素，并移动它到上面的位置
        # smallImage = self.driver.find_element(By.XPATH,
        #                                       "//*[@id='tCaptchaDyMainWrap']/div[2]/div[2]/div[2]/div/div")
        smallImage = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='tCaptchaDyMainWrap']/div[2]/div[2]/div[2]/div/div"))
        )
        # 小滑块到目标区域的移动距离（新缺口的水平坐标-小滑块的水平坐标）
        # 新缺口坐标=原缺口坐标*新画布宽度/原画布宽度
        newDis = int(dis * 330 / 672 - 35)
        # 添加调试输出验证计算值
        print(
            f"老画布宽：672，老缺口x坐标dis:{dis} | 新画布宽：330，新缺口x坐标:{dis * 330 / 672} | 小滑块初始x坐标:30 | 计算移动距离:{newDis}")
        time.sleep(1)

        # 按下小滑块按钮不动
        ActionChains(self.driver).click_and_hold(smallImage).perform()
        # 移动小滑块，模拟人的操作，一次次移动一点点
        i = 0
        moved = 0
        while moved < newDis:
            x = random.randint(3, 10)  # 每次移动3到10像素
            moved += x
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
            # print("第{}次移动后，位置为{}".format(i, smallImage.location['x']))
            i += 1
        # 移动完之后，松开鼠标
        ActionChains(self.driver).release().perform()
        time.sleep(5)
        logger.info("登录成功")
        allure.attach(self.driver.get_screenshot_as_png(), "登录成功截图", allure.attachment_type.PNG)  # 交互后截图

        # ActionChains(self.driver).click_and_hold(smallImage).perform()
        # # 轨迹参数
        # total_move = newDis
        # moved = 0
        # base_speed = [3, 5, 8, 12]  # 不同阶段的基础速度
        # while moved < total_move:
        #     # 分阶段调整速度
        #     if moved < total_move * 0.3:
        #         speed = random.choice(base_speed[:2])  # 初始慢速
        #     elif moved < total_move * 0.8:
        #         speed = random.choice(base_speed[2:])  # 中段加速
        #     else:
        #         speed = random.choice([1, 2])  # 末尾减速
        #
        #     # 添加垂直抖动
        #     y_jitter = random.randint(-2, 2)
        #
        #     ActionChains(self.driver).move_by_offset(
        #         xoffset=speed,
        #         yoffset=y_jitter
        #     ).perform()
        #
        #     moved += speed
        #     time.sleep(random.uniform(0.05, 0.2))  # 随机停顿
        #
        # # 添加最终微调抖动
        # for _ in range(3):
        #     ActionChains(self.driver).move_by_offset(
        #         xoffset=random.choice([-1, 0, 1]),
        #         yoffset=random.choice([-1, 0, 1])
        #     ).perform()
        #
        # ActionChains(self.driver).release().perform()
        # time.sleep(5)
        # logger.info("登录成功")
        # allure.attach(self.driver.get_screenshot_as_png(), "登录成功截图", allure.attachment_type.PNG)  # 交互后截图

    def get_pos(self, imageSrc):
        # 读取图像文件并返回一个image数组表示的图像对象
        image = cv2.imread(imageSrc)
        # GaussianBlur方法进行图像模糊化/降噪操作。
        # 它基于高斯函数（也称为正态分布）创建一个卷积核（或称为滤波器），该卷积核应用于图像上的每个像素点。
        blurred = cv2.GaussianBlur(image, (5, 5), 0, 0)
        # Canny方法进行图像边缘检测
        # image: 输入的单通道灰度图像。
        # threshold1: 第一个阈值，用于边缘链接。一般设置为较小的值。
        # threshold2: 第二个阈值，用于边缘链接和强边缘的筛选。一般设置为较大的值
        canny = cv2.Canny(blurred, 0, 100)  # 轮廓
        # findContours方法用于检测图像中的轮廓,并返回一个包含所有检测到轮廓的列表。
        # contours(可选): 输出的轮廓列表。每个轮廓都表示为一个点集。
        # hierarchy(可选): 输出的轮廓层次结构信息。它描述了轮廓之间的关系，例如父子关系等。
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # 遍历检测到的所有轮廓的列表
        for contour in contours:
            # contourArea方法用于计算轮廓的面积
            area = cv2.contourArea(contour)
            # arcLength方法用于计算轮廓的周长或弧长
            length = cv2.arcLength(contour, True)
            # 如果检测区域面积在5025-7225之间，周长在300-380之间，则是目标区域
            if 5025 < area < 7225 and 300 < length < 380:
                # 计算轮廓的边界矩形，得到坐标和宽高
                # x, y: 边界矩形左上角点的坐标。
                # w, h: 边界矩形的宽度和高度。
                x, y, w, h = cv2.boundingRect(contour)
                print("计算出老画布缺口位置的坐标及宽高：", x, y, w, h)
                # 在目标区域上画一个红框看看效果
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.imwrite("./testcases/old_square.jpg", image)
                return x
        return 0


# 发送常量短信
class TestSendConstantSmsPage(TestBasePage):
    def __init__(self, driver):
        super().__init__(driver)  # 调用基类构造函数
        self.marketingSms = "//*[@id='clApp']/div/div[3]/div/div/div/div[1]/div/div[3]/div/div[2]/div/div/div//div[text()='会员营销短信']"
        self.smsSend = "//*[@id='childRoot']/div/div[1]/div/div/div/div/div[3]/div/a[1]"
        self.smsBatchSendBtn = "//*[@id='childRoot']/div/div[2]/div/div/div[1]/div/div[3]/button/span"
        self.manualAdd = "//*[@id='onlinesendForm']/div[2]/div[2]/div/div/div/div[3]/button/span[2]"
        self.inputMobile = "/html/body/div[4]/div/div[2]/div/div[2]/div[2]/div[2]/span/input"
        self.confirmBtn = "/html/body/div[4]/div/div[2]/div/div[2]/div[3]/button[2]/span"
        self.selectTemplate = "//*[@id='onlinesendForm']/div[4]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/span[2]"
        self.inputTemplateContent = "//div[@class='sms-modal-body']//input[@placeholder='请输入模板内容']"
        self.searchBtn = "//div[@class='sms-modal-body']//span[@class='anticon']"
        self.select = "//div[@class='sms-table-body']//a"
        self.submitSmsBatchTask = "//*[@id='onlinesendForm']/div[8]/div/div/div/div/div[2]/button/span"
        self.sendNow = "//div[@class='sms-modal-body']//span[text()='立即发送']"
        self.result = "//div[@class='ant-modal-body']//div[@class='ant-modal-confirm-content']"

    def sendConstantSms(self,env_config):
        logger.info("准备发送常量短信")
        self.get_element(self.marketingSms).click()
        self.get_element(self.smsSend).click()
        self.get_element(self.smsBatchSendBtn).click()
        self.get_element(self.manualAdd).click()
        self.get_element(self.inputMobile).send_keys("15274438093,13203173318,19074910586")
        self.get_element(self.confirmBtn).click()
        time.sleep(3)  # 等待号码输入框关闭
        self.get_element(self.selectTemplate).click()
        constantTemplate = f"{env_config['constantTemplate']}"
        self.get_element(self.inputTemplateContent).send_keys(constantTemplate)
        self.get_element(self.searchBtn).click()
        time.sleep(3)  # 等待搜索完成
        self.get_element(self.select).click()
        time.sleep(3)  # 等待选择模板框关闭
        self.get_element(self.submitSmsBatchTask).click()
        self.get_element(self.sendNow).click()
        logger.info("发送常量短信完成")
        allure.attach(self.driver.get_screenshot_as_png(), "常量短信发送成功截图", allure.attachment_type.PNG)  # 交互后截图


# 发送变量短信
class TestSendVariableSmsPage(TestSendConstantSmsPage):
    def __init__(self, driver):
        super().__init__(driver)  # 调用基类构造函数
        self.variableSmsSend = "//*[@id='childRoot']/div/div[1]/div/div/div/div/div[3]/div/a[2]"
        self.smsBatchSendBtn = "//*[@id='childRoot']/div/div[2]/div/div/div[1]/div/div[3]/div/button/span"
        self.insertVariableContent = "//*[@id='onlinesendForm']/div[3]/div[2]/div/div/div[1]/div/button/span[2]"
        self.fileInputLocator = "//div[@class='sms-modal-body']//input"
        self.beginUpload = "//div[@class='sms-modal-body']//span[text()='开始上传']"


    def sendVariableSms(self,env_config):
        logger.info("准备发送变量短信")
        variableSend_url = f"{env_config['variableSend_url']}"
        self.driver.get(variableSend_url)
        self.get_element(self.variableSmsSend).click()
        self.get_element(self.smsBatchSendBtn).click()
        self.get_element(self.insertVariableContent).click()

        file_input = self.driver.find_element(By.XPATH, self.fileInputLocator)
        self.driver.execute_script(
            "arguments[0].style.display='block'; arguments[0].click();",
            file_input
        )
        file_input.send_keys('C:\\Users\\15274\\Downloads\\guoneibianliang.txt')

        self.get_element(self.beginUpload).click()
        time.sleep(10)  # 等待变量上传框关闭
        self.get_element(self.selectTemplate).click()
        variableTemplate = f"{env_config['variableTemplate']}"
        self.get_element(self.inputTemplateContent).send_keys(variableTemplate)
        self.get_element(self.searchBtn).click()
        time.sleep(3)  # 等待搜索完成
        self.get_element(self.select).click()
        time.sleep(3)  # 等待选择模板框关闭
        self.get_element(self.submitSmsBatchTask).click()
        self.get_element(self.sendNow).click()
        logger.info("发送变量短信完成")
        allure.attach(self.driver.get_screenshot_as_png(), "变量短信发送成功截图", allure.attachment_type.PNG)  # 交互后截图
