from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from geetestverify import GeetestVerify

# 代理服务器
proxyHost = "222.241.68.3"
proxyPort = "4252"
proxyType = 'https'  # socks5

# 代理隧道验证信息
service_args = [
    "--proxy-type=%s" % proxyType,
    "--proxy=%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
    }
    ]
options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"')


DRIVER_PATH = "f:/Users/olivertian/Desktop/spider/spider_work/ChromeDriver/chromedriver.exe"
browser = webdriver.Chrome(DRIVER_PATH, service_args=service_args, chrome_options=options)
wait = WebDriverWait(browser, 5)

browser.get("https://www.baidu.com/s?tn=50000021_hao_pg&ie=utf-8&sc=UWd1pgw-pA7EnHc1FMf"
            "qnHRvn1b1P1fvP1csPauW5y99U1Dznzu9m1YzP1TzPjb1PHD1&ssl_sample=normal&srcqid=3320355327482831510&H123Tmp=nunew7&word=ip")
browser.execute_script("window.open('https://passport.bilibili.com/login')")  # 新建窗口打开
browser.switch_to.window(browser.window_handles[1])  # 切换窗口

# browser.get("https://passport.bilibili.com/login")

input_name = browser.find_element_by_css_selector("#login-username")
input_pwd = browser.find_element_by_css_selector("#login-passwd")
submit_btn = browser.find_element_by_css_selector(".btn.btn-login")
input_name.send_keys("13066882860")
input_pwd.send_keys("sjgkjfg12344")
time.sleep(5)
submit_btn.click()
g = GeetestVerify(browser)
while True:
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".geetest_canvas_img.geetest_absolute")))
        g.geetest_init()
        g.move_to_gap()
        break
    except TimeoutException:
        input_name.clear()
        input_pwd.clear()
        input_name.send_keys("13066882860")
        input_pwd.send_keys("181855makesi")
        time.sleep(5)
        submit_btn.click()


#  ***************************** 分界线 ******************************

# proxyauth_plugin_path = create_proxyauth_extension(
#     proxy_host="https://113.116.244.233:56",
#     proxy_port="56",
#     proxy_username="olivertian",
#     proxy_password="181855makesi"
# )
# browser = webdriver.Chrome(DRIVER_PATH)
# wait = WebDriverWait(browser, 2)
# browser.get("https://passport.lagou.com/login/login.html?service=https%3a%2f%2fwww.lagou.com%2f")


# chromeOptions.add_extension(proxyauth_plugin_path)
# chromeOptions.add_argument("--proxy-server=https://113.116.244.233:56")
# browser = webdriver.Chrome(DRIVER_PATH, chrome_options=chromeOptions)
# browser.get("https://httpbin.org/ip")
# browser.get("https://www.baidu.com/s?tn=50000021_hao_pg&ie=utf-8&sc=UWd1pgw-pA7EnHc1FMfqnHRvn1b1P1fvP1csPauW5y99U1Dznzu9m1YzP1TzPjb1PHD1&ssl_sample=normal&srcqid=3320355327482831510&H123Tmp=nunew7&word=ip")
# print(browser.page_source)
# browser.get("https://www.baidu.com/s?tn=50000021_hao_pg&ie=utf-8&sc=UWd1pgw-pA7EnHc1FMfqnHRvn1b1P1fvP1csPauW5y99U1Dznzu9m1YzP1TzPjb1PHD1&ssl_sample=normal&srcqid=3320355327482831510&H123Tmp=nunew7&word=ip")
# print(browser.page_source)
# browser.quit()




