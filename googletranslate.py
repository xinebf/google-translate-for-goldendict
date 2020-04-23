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
import asyncio
from functools import partial
import re


def get_url(tl, qry):
    url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={tl}&dt=t&q={qry}'
    return url


def get_resp(url):
    base_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    session = requests.Session()
    session.headers = base_headers
    resp = session.get(url, timeout=5).json()
    return resp


def get_result(resp, result):
    for x in resp[0]:
        result += x[0] if x[0] else ''
    result += '\n'
    return result


def result_to_html(result):
    css_text = """\
    <style type="text/css">
    p {white-space: pre-wrap;}
    gray {color: #606060;}
    </style>"""
    match = re.compile(rf"({re.escape('^_^')}: Translate)(.*)(To)(.*)")
    result = match.sub(r'<gray>\1</gray>\2<gray>\3</gray>\4', result)
    result = f'<html>\n<head>\n{css_text}\n</head>\n<body>\n<p>{result}</p>\n</body>\n</html>'
    return result


async def gtrans():
    result = ''
    sys.stdout.reconfigure(encoding='utf-8')
    qry = urllib.parse.quote_plus(sys.argv[2])
    url = get_url(sys.argv[1], qry)
    url_alt = get_url(atl, qry)
    try:
        loop = asyncio.get_running_loop()
        resp = loop.run_in_executor(None, partial(get_resp, url))
        resp_alt = loop.run_in_executor(None, partial(get_resp, url_alt))
        [resp, resp_alt] = await asyncio.gather(resp, resp_alt)
        if resp[2] == sys.argv[1]:
            result += f'^_^: Translate {resp[2]} To {atl}\n'
            result = get_result(resp, result)
            result = get_result(resp_alt, result)
        else:
            result += f'^_^: Translate {resp[2]} To {sys.argv[1]}\n{sys.argv[2]}\n'
            result = get_result(resp, result)
        result = result_to_html(result)
        print(result.encode('utf-8', 'ignore').decode('utf-8'))
    except requests.exceptions.ReadTimeout as e:
        print('╰（‵□′）╯: ReadTimeout...')
    except Exception as e:
        return f'Errrrrrrrrror {e}'


if __name__ == "__main__":
    atl = 'en'
    asyncio.run(gtrans())
