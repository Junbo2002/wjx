from concurrent.futures.thread import ThreadPoolExecutor
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import fun
import short_answer
import proxy_util


chrome_options = Options()
# 设置无头浏览器
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 滑块防止检测
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver_path = 'C:\Program Files\Google\Chrome\Application\chromedriver'
# driver_path = ''
head = '(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))'
proxy_list = proxy_util.update_proxy()

# 每个问题选项的数量（-1表示该题为简答题）
option_nums = [2, 4, 6, 2, -1, 3, 2, 3, 3, -1, 2, 2, 2, 2, 3, -1, 3, -1]  # 18
# 0表示单选，1表示多选
multiple_choice = [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def solve(cnt: int):

    # 设置代理
    PROXY = proxy_util.random_proxy(proxy_list)  # 随机用一个代理
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",
    }

    driver = webdriver.Chrome(driver_path, options=chrome_options)
    # 设置最大连接时间，超时抛出异常
    # driver.set_page_load_timeout(10)

    # 设置浏览器定位
    (longitude, latitude) = fun.random_position()
    # print(longitude, latitude)
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": 100
    })
    # 将webdriver属性置为undefined
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                        {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })

    # 打开问卷星网址
    driver.get('https://www.wjx.cn/vm/tuhQw9L.aspx')

    # driver.maximize_window()
    # 每个问题的选项
    q_num = len(option_nums)

    for i in range(0, q_num):
        # 第i+1题目的选项数
        num = option_nums[i]
        if num == -1:
            # 简答题
            text_input = driver.find_element(By.XPATH, f'//*[@id="div{i+1}"]/div[1]/div/label/span')
            text_input.clear()
            text = short_answer.get_short_answer(i+1)
            text_input.send_keys(text)

        elif multiple_choice[i] == 0:
            # 单选题
            q_option = fun.random_option(num)
            q_select = driver.find_element(By.XPATH, f'//*[@id="div{i+1}"]/div[2]/div[{q_option}]')
            q_select.click()
        else:
            # 多选题
            q_selects = fun.random_multi_select(num)
            for j in q_selects:
                q_select = driver.find_element(By.XPATH, f'//*[@id="div{i+1}"]/div[2]/div[{j}]')
                q_select.click()

    submit_button = driver.find_element(By.XPATH, '//*[@id="ctlNext"]')
    submit_button.click()
    time.sleep(0.2)
    confirm = driver.find_element(By.XPATH, '//*[@id="alert_box"]/div[2]/div[2]/button')
    confirm.click()
    validation = driver.find_element(By.XPATH, '//*[@id="rectMask"]')
    validation.click()
    time.sleep(2.5)

    res = driver.find_element(By.XPATH, '//*[@id="SM_TXT_1"]')

    # 滑块验证
    try:
        slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')

        print('[' + eval(head) + f']: ', slider.text, cnt)
        if str(slider.text).startswith("请按住滑块"):
            width = slider.size.get('width')
            ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()

    except selenium.common.exceptions.NoSuchElementException:
        pass

    time.sleep(1)
    print('[' + eval(head) + f']: ', res.text, cnt)
    driver.close()


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=1)
    current_time = int(time.time())
    last_time = current_time
    for i in range(1000000):
        pool.submit(solve, i+1)

        current_time = int(time.time())
        gap = current_time - last_time
        # 8分钟更新一次代理
        if gap >= 480:
            proxy_list = proxy_util.update_proxy()
            print('[' + eval(head) + ']: 更新代理列表')
            last_time = current_time

