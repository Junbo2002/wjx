import random

import requests
import time

head = '(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))'


def update_proxy():
    url = 'http://120.48.78.248:8000/proxy'
    param = {
        "key": "junbo",
        "num": "40"
    }
    resp = requests.get(url=url, params=param)
    proxy_list = list(resp.json())

    print('[' + eval(head) + f']: 更新代理列表,最近更新时间:', proxy_list[0], ' UTC')
    proxy_list.pop(0)
    return proxy_list


def random_proxy(proxy_list: list):
    length = len(proxy_list)
    index = random.randint(0, length-1)
    return proxy_list[index]


if __name__ == '__main__':
    pl = update_proxy()
    print(pl)
    print(len(pl))