from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.action_chains import ActionChains


class GeetestVerify(object):
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 10)

    def geetest_init(self):
        self.hide_slider()  # 一开始就要隐藏掉滑块，避免干扰到缺口的定位（因为fullbg是不会显示滑块的）

    def hide_slider(self):
        hiden_slider = "document.querySelector('.geetest_canvas_slice.geetest_absolute').style.display='none';"
        self.browser.execute_script(hiden_slider)  # 隐藏滑块

    def show_slider(self):
        show_slider = "document.querySelector('.geetest_canvas_slice.geetest_absolute').style.display='block';"
        self.browser.execute_script(show_slider)  # 显示滑块

    def hide_gap(self):
        hiden_gap = "document.querySelector('.geetest_canvas_fullbg.geetest_fade.geetest_absolute').style.display='block';"
        self.browser.execute_script(hiden_gap)  # 显示没有缺口的背景，即干净的背景图

    def show_gap(self):
        show_gap = "document.querySelector('.geetest_canvas_fullbg.geetest_fade.geetest_absolute').style.display='none';"
        self.browser.execute_script(show_gap)  # 显示有缺口的背景

    def get_fullbg_img(self):
        """把缺口隐藏 --> 截浏览器窗口图 --> 计算fullbg的四角坐标 --> 裁剪得到fullbg"""
        self.hide_gap()  # 隐藏缺口
        full_bg_img = self.get_geetest_image()  # 获取裁剪的fullbg
        return full_bg_img

    def get_gapbg_img(self):
        """显示缺口 --> 截浏览器窗口图 --> 计算gapbg的四角坐标 --> 裁剪得到gapbg"""
        self.show_gap()  # 缺口显示
        gap_bg_img = self.get_geetest_image()  # 获取裁剪的gapbg
        return gap_bg_img

    def get_screenshot(self):
        """获取浏览器窗口截图"""
        screenshot = self.browser.get_screenshot_as_png()  # screenshot是二进制数据
        f = BytesIO(screenshot)  # 理解为创建一个位于内存(RAM)中的文件f，BytesIO将screenshot读到内存，而不是open("xx","wb")写入硬盘文件的方式
        screenshot = Image.open(f)
        return screenshot

    def get_position(self):
        """获取背景图片四角坐标"""
        img = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".geetest_canvas_bg.geetest_absolute")))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location["y"], location["y"] + size["height"], location["x"], location["x"] + size["width"]
        return left, top, right, bottom  # 注意顺序是左上右下

    def get_geetest_image(self):
        """裁剪背景图片"""
        left, top, right, bottom = self.get_position()
        screenshot = self.get_screenshot()
        captcha_crop = screenshot.crop((left, top, right, bottom))
        return captcha_crop  # image对象

    def is_pixel_equal(self, img1, img2, x, y):
        """判断两张背景图片相同地方的像素点GRB值是否相同"""
        pixel1 = img1.load()[x, y]
        pixel2 = img2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        """获取缺口最左侧位置"""
        left = 20
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def get_track(self, distance):
        """生成轨迹列表"""
        track = []
        current = 10
        mid = distance * 4 / 5
        t = 0.2
        v = 0

        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))  # round四舍五入，第二个参数忽略则默认为0，即四舍五入保留整数部分
        return track

    def move_to_gap(self):
        """滑块移动到缺口位置"""
        gapbg_img = self.get_gapbg_img()  # 获取缺口背景图
        fullbg_img = self.get_fullbg_img()  # 获取无缺口背景图
        gap_left = self.get_gap(gapbg_img, fullbg_img)  # 获取缺口左侧位置
        tracks = self.get_track(gap_left)  # 根据缺口左侧位置生成轨迹列表

        self.show_slider()  # 显示滑块
        self.show_gap()  # 显示缺口

        sliderbar = self.browser.find_element_by_css_selector(".geetest_slider_button")  # 获取滑块元素
        ActionChains(self.browser).click_and_hold(sliderbar).perform()
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()
