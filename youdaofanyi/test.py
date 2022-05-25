import time

import requests
import json
from hashlib import md5
import random

post_url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
appVersion = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"


def r(e):
    t = md5(appVersion.encode()).hexdigest()
    r = str(int(time.time() * 1000))
    i = r + str(random.randint(0, 9))

    return {
        'ts': r,
        'bv': t,
        'salt': i,
        'sign': md5(("fanyideskweb" + e + i + "Ygy_4c=r#e#4EX^NUGUc5").encode()).hexdigest()
    }


def fanyi(word):
    data1 = r(word)
    # print(data)
    headers = {
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': appVersion,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://fanyi.youdao.com/',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'smartresult': [
            'dict',
            'rule',
        ],
    }

    data_json = {
        'i': word,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': data1['salt'],
        'sign': data1['sign'],
        'lts': data1['ts'],
        'bv': data1['bv'],
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME',
    }

    res = requests.post(post_url, params=params, headers=headers, data=data_json)
    return res.json()


if __name__ == '__main__':
    while True:
        word = input('请输入你想要翻译的内容：')
        results = fanyi(word)
        print(results)
