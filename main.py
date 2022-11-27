from selenium import webdriver
import random,os,time,json
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from concurrent.futures.thread import ThreadPoolExecutor
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options





def random_proxy(proxy_list: list):
    length = len(proxy_list)
    index = random.randint(0, length-1)
    return proxy_list[index]


provinces = {
    '吉林省': [125.326800, 43.896160], '黑龙江省': [126.662850, 45.742080],
    '辽宁省': [123.429250, 41.835710], '内蒙古自治区': [111.765220, 40.817330],
    '新疆维吾尔自治区': [87.627100, 43.793430], '青海省': [101.780110, 36.620870],
    '北京市': [116.407170, 39.904690], '天津市': [117.199370, 39.085100],
    '上海市': [121.473700, 31.230370], '重庆市': [106.550730, 29.564710],
    '河北省': [114.469790, 38.035990], '河南省': [113.753220, 34.765710],
    '陕西省': [108.954240, 34.264860], '江苏省': [118.762950, 32.060710],
    '山东省': [117.020760, 36.668260], '山西省': [112.562720, 37.873430],
    '甘肃省': [103.826340, 36.059420], '宁夏回族自治区': [106.258670, 38.471170],
    '四川省': [104.075720, 30.650890], '西藏自治区': [91.117480, 29.647250],
    '安徽省': [117.285650, 31.861570], '浙江省': [120.153600, 30.265550],
    '湖北省': [114.342340, 30.545390], '湖南省': [112.983400, 28.112660],
    '福建省': [119.296590, 26.099820], '江西省': [115.910040, 28.674170],
    '贵州省': [106.707220, 26.598200], '云南省': [102.709730, 25.045300],
    '广东省': [113.266270, 23.131710], '广西壮族自治区': [108.327540, 22.815210],
    '香港': [114.165460, 22.275340], '澳门': [113.549130, 22.198750],
    '海南省': [110.348630, 20.019970], '台湾省': [121.520076, 25.030724],
}


def random_option(num: int):
    x = random.randint(1, num)
    # print(x)
    return x


def random_multi_select(num: int):
    # 多选的数量
    length = random_option(num)
    pre = []
    # 顺序排序
    for i in range(1, num+1):
        pre.append(i)

    # 洗牌算法
    index = num - 1  # 从数组的最后一个数（下标为i）开始
    while index > 0:
        index_2 = random.randint(0, index)
        # 将得到的下标对应的元素和最后一个数交换
        pre[index], pre[index_2] = pre[index_2], pre[index]
        # 将最后一个数拿出数组
        index -= 1
    return pre[0:length]


def random_position():
    index = random.randint(0, len(provinces)-1)
    return list(provinces.values())[index]


chrome_options = Options()
# 设置无头浏览器
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 滑块防止检测
chrome_options.add_argument("--incognito") 
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver_path = Service('C:\Program Files\Google\Chrome\Application\chromedriver.exe')
# driver_path = ''
head = '(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))'




if os.path.isfile("config.json"):
    with open("config.json",encoding='utf8') as f:
        x = json.load(f)
        option_nums = x["option_nums"]
        multiple_choice = x["multiple_choice"]
        max_workers = x["max_workers"]
        run_num = x["run_num"]
        url = x["url"]
else:
    with open("config.json","w+",encoding='utf8') as f:
        f.write("""
{
    "option_nums":[2, 5, 4, 4, 4, 5, 2], 
    "注释1": "每个问题选项的数量（-1表示该题为简答题）",
    "multiple_choice":[0,0,0,0,0,1,0],
    "注释2": " 0表单选 1表多选 简答题随意",
    "max_workers" : 4, 
    "注释3": "//线程数量",
    "run_num" : 200 , 
    "注释4": "//填写问卷次数",
    "url" : "https://www.wjx.cn/vm/exnm04A.aspx",
    "注释5" : "调查问卷链接"
}"""
        )
    print(
        """
        ##########################################
        ##########################################
                      配置文件已生成

            请填写config.json文件后再次运行此文件
            
        ##########################################
        ##########################################
        """
    )
    exit()


def solve(cnt: int):

    #设置代理 如果有请自行填写
    # PROXY = random_proxy()  # 随机用一个代理

    # webdriver.DesiredCapabilities.CHROME['proxy'] = {
    #     "httpProxy": PROXY,
    #     "ftpProxy": PROXY,
    #     "sslProxy": PROXY,
    #     "proxyType": "MANUAL",
    # }

    driver = webdriver.Chrome(service=driver_path, options=chrome_options)
    driver.implicitly_wait(10)
    # 设置最大连接时间，超时抛出异常
    driver.set_page_load_timeout(10)

    # 设置浏览器定位
    (longitude, latitude) = random_position()
    # print(longitude, latitude)
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": 100
    })
    # 将webdriver属性置为undefined
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator,'webdriver',{
                get: () => undefined
            })
        """
    })
    # 打开问卷星网址
    driver.get(url)

    # driver.maximize_window()
    # 每个问题的选项
    q_num = len(option_nums)

    for i in range(0, q_num):
        # 第i+1题目的选项数
        num = option_nums[i]
        if num == -1:
            # 简答题
            text_input = driver.find_element(By.ID, f'q{i+1}')
            text_input.clear()
            text_input.send_keys("无")

        elif multiple_choice[i] == 0:
            # 单选题
            q_option = random_option(num)
            driver.find_element(By.XPATH, f'//*[@id="div{i+1}"]/div[2]/div[{q_option}]').click()

        else:
            # 多选题
            q_selects = random_multi_select(num)
            for j in q_selects:
                driver.find_element(By.XPATH, f'//*[@id="div{i+1}"]/div[2]/div[{j}]').click()
                
    driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
    driver.find_element(By.CLASS_NAME, 'layui-layer-btn0').click()
    driver.find_element(By.XPATH, '//*[@id="rectMask"]').click()


    

    # 滑块验证
    try:
        slider = driver.find_element(By.CLASS_NAME, 'nc-lang-cnt')

        print('[' + eval(head) + f']: ', slider.text, cnt)
        if str(slider.text).startswith("请按住滑块"):
            width = slider.size.get('width')
            ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()

    except NoSuchElementException:
        pass
    res = driver.find_element(By.ID, 'divdsc')
    print('[' + eval(head) + f']: ',res.text, cnt)
    driver.close()



if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=max_workers)
    for i in range(run_num):
        pool.submit(solve, i+1)



