#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Get translate from Google Translate
author: 'ZHANGXINZENG'
Created on 2018-04-18 17:04:00
USAGE:
python3 googletranslate.py <target language code> <text to be translated>
python googletranslate.py zh-CN 'hello world!'
"""

import requests
import sys
import urllib.parse


def get_url(tl, qry):
    url = 'https://{}/translate_a/single?client=gtx&sl=auto&tl={}&dt=at&dt=bd&dt=ex&' \
          'dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&q={}'.format(http_host, tl, qry)
    return url


def get_synonym(result, resp):
    if resp[1]:
        result = result + '\n=========\n'
        result = result + '0_0: Translations of {}\n'.format(sys.argv[2])
        for x in resp[1]:
            result = result + '{}.\n'.format(x[0][0])
            for i in x[2]:
                result = result + '{}: {}\n'.format(i[0], ", ".join(i[1]))
    return result


def get_result(results, resp):
    for x in resp[0]:
        if x[0]:
            results = results + x[0]
    return results


def get_translation():
    if len(sys.argv[2]) > 5000:
        print('(╯‵□′)╯︵┻━┻: Maximum characters exceeded...')
        return
    result = ''
    base_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    session = requests.Session()
    session.headers = base_headers
    parse_query = urllib.parse.quote_plus(sys.argv[2])
    url = get_url(sys.argv[1], parse_query)
    try:
        resp = session.get(url, timeout=3).json()
        if resp[2] == sys.argv[1]:
            result = result + '^_^: Translate {} To {}\n'.format(resp[2], alternative_language)
            url = get_url(alternative_language, parse_query)
            resp_en = session.get(url, timeout=3).json()
            result = get_result(result, resp_en)
            result = result + '\n'
        else:
            result = result + '^_^: Translate {} To {}\n{}\n'.format(resp[2], sys.argv[1], sys.argv[2])
        result = get_result(result, resp)
        if resp[2] == sys.argv[1]:
            result = get_synonym(result, resp_en)
        else:
            result = get_synonym(result, resp)
        print(result.encode(result_code, 'ignore').decode(result_code))
    except requests.exceptions.ReadTimeout:
        print('╰（‵□′）╯: ReadTimeout...')


if __name__ == "__main__":
    http_host = 'translate.googleapis.com'
    result_code = 'gbk'
    alternative_language = 'en'
    get_translation()
