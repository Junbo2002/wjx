from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import proxy_util
import time
import requests
import re

chrome_options = Options()
# 设置无头浏览器
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

proxy_list = []
# proxy_util.update_proxy(proxy_list)
# proxy = proxy_util.random_proxy(proxy_list)

# 设置代理
# PROXY='80.48.119.28:8080'
# webdriver.DesiredCapabilities.CHROME['proxy'] = {
#     "httpProxy": PROXY,
#     "ftpProxy": PROXY,
#     "sslProxy": PROXY,
#     "proxyType": "MANUAL",
#
# }

# driver_path = 'C:\Program Files\Google\Chrome\Application\chromedriver'
# driver = webdriver.Chrome(options=chrome_options)
# url1 = "https://www.google.com"
# url2 = 'https://www.wjx.cn/vm/tuhQw9L.aspx'
# driver.get(url1)
# print(driver.page_source)
# driver.close()

# 获取网页源码
# result = driver.find_element(by=By.XPATH, value='//*[@class="result"]')
# print(result.text)

proxies={
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}
url = 'https://free-proxy-list.net/'
resp = requests.get(url, proxies=proxies)
# print(resp.text)
re = re.compile('\d+.\d+.\d+.\d+:\d+')
res = re.finditer(resp.text)

for it in res:
    print(it.group())