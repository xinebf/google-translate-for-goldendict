#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Get translate from Google Translate
author: 'XINZENG ZHANG'
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
        result = result + '0_0: Translations of {}\n'.format(query_string)
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


def get_definitions(result, resp):
    result = result + '\n=========\n'
    result = result + '^_^: Definitions of {}\n'.format(query_string)
    for x in resp[12]:
        result = result + '{}.\n'.format(x[0])
        for y in x[1]:
            result = result + '  - {}\n    * {}\n'.format(y[0], y[2])
    return result


def get_examples(result, resp):
    result = result + '\n=========\n'
    result = result + '^_^: Examples of {}\n'.format(query_string)
    for x in resp[13][0]:
        result = result + '  - {}\n'.format(x[0].replace("<b>", "").replace("</b>", ""))
    return result


def get_translation():
    if len(query_string) > 5000:
        print('(╯‵□′)╯︵┻━┻: Maximum characters exceeded...')
        return
    result = ''
    base_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    session = requests.Session()
    session.headers = base_headers
    parse_query = urllib.parse.quote_plus(query_string)
    url = get_url(target_language, parse_query)
    try:
        resp = session.get(url, timeout=3).json()
        if resp[2] == target_language:
            result = result + '^_^: Translate {} To {}\n'.format(resp[2], alternative_language)
            url = get_url(alternative_language, parse_query)
            resp_en = session.get(url, timeout=3).json()
            result = get_result(result, resp_en)
            result = result + '\n'
        else:
            result = result + '^_^: Translate {} To {}\n{}\n'.format(resp[2], target_language, query_string)
        result = get_result(result, resp)
        if resp[2] == target_language:
            result = get_synonym(result, resp_en)
        else:
            result = get_synonym(result, resp)
        if definitions_examples:
            if len(resp) >= 13 and resp[12]:
                result = get_definitions(result, resp)
            if len(resp) >= 14 and resp[13]:
                result = get_examples(result, resp)
        print(result.encode(result_code, 'ignore').decode(result_code))
    except requests.exceptions.ReadTimeout:
        print('╰（‵□′）╯: ReadTimeout...')


if __name__ == "__main__":
    http_host = 'translate.googleapis.com'
    target_language = sys.argv[1]
    query_string = sys.argv[2]
    definitions_examples = True
    result_code = 'gbk'
    alternative_language = 'en'
    get_translation()
