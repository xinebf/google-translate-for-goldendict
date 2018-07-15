#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Get translate from Google Translate
author: 'ZHANGXINZENG'
Created on 2018-04-18 17:04:00
USAGE:
python3 googletranslate.py <target language code> <text to be translated>
python googletranslate.py zh-CN 'hello world!'
'''

import requests
import sys
import urllib.parse

proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080"
}

def gtrans():
    result = ''
    base_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    session = requests.Session()
    session.headers = base_headers
    qry = urllib.parse.quote_plus(sys.argv[2])
    url = 'http://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={}&dt=t&q={}'.format(sys.argv[1], qry)
    try:
        resp = session.get(url, proxies=proxies, timeout=3).json()[0]
        for x in resp:
            result = result + x[0]
        print(result.encode('gbk', 'ignore').decode('gbk'))
    except requests.exceptions.ReadTimeout as e:
        print('╰（‵□′）╯: ReadTimeout...')
    except requests.exceptions.ProxyError as e:
        print('(╯‵□′)╯︵┻━┻: ProxyError...')

if __name__ == "__main__":
    gtrans()
