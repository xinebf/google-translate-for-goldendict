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
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={}&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&q={}'.format(sys.argv[1], qry)
    try:
        resp = session.get(url, timeout=3).json()
        if resp[2] == "zh-CN":
            result = result + '^_^: Translate {} To {}\n'.format(resp[2], atl)
            url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={}&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&q={}'.format(atl, qry)
            respen = session.get(url, timeout=3).json()
            for x in respen[0]:
                if not x[0] is None:
                    result = result + x[0]
            result = result + '\n'
        else:
            result = result + '^_^: Translate {} To {}\n{}\n'.format(resp[2], sys.argv[1], sys.argv[2])
        for x in resp[0]:
            if not x[0] is None:
                result = result + x[0]
        if resp[2] == "zh-CN":
            if not respen[1] is None:
                result = result + '\n=========\n'
                result = result + '0_0: Translations of {}\n'.format(sys.argv[2])
                for x in respen[1]:
                    result = result + '{}\n'.format(x[0][0])
                    for i in x[2]:
                        result = result + '{}: {}\n'.format(i[0], ", ".join(i[1]))
        else:
            if not resp[1] is None:
                result = result + '\n=========\n'
                result = result + '0_0: Translations of {}\n'.format(sys.argv[2])
                for x in resp[1]:
                    result = result + '{}\n'.format(x[0][0])
                    for i in x[2]:
                        result = result + '{}: {}\n'.format(i[0], ", ".join(i[1]))
        print(result.encode('gbk', 'ignore').decode('gbk'))
    except requests.exceptions.ReadTimeout as e:
        print('╰（‵□′）╯: ReadTimeout...')

if __name__ == "__main__":
    atl = 'en'
    gtrans()
