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

def gtrans():
    result = ''
    base_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    session = requests.Session()
    session.headers = base_headers
    qry = urllib.parse.quote_plus(sys.argv[2])
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={}&dt=t&q={}'.format(sys.argv[1], qry)
    try:
        resp = session.get(url, timeout=3).json()
        result = result + '^_^: Translate {} To {}\n{}\n'.format(resp[2], sys.argv[1], sys.argv[2])
        for x in resp[0]:
            result = result + x[0]
        print(result.encode('gbk', 'ignore').decode('gbk'))
    except requests.exceptions.ReadTimeout as e:
        print('╰（‵□′）╯: ReadTimeout...')

if __name__ == "__main__":
    gtrans()
