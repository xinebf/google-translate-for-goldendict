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
import asyncio
from functools import partial
import re
import argparse
from googletranslatetk import Token


class GoogleTranslate(object):
    def __init__(self, args):
        self.http_host = args.host
        self.http_proxy = args.proxy
        self.synonyms_en = args.synonyms
        self.definitions_en = args.definitions
        self.examples_en = args.examples
        self.result_code = 'utf-8' if args.type == 'html' else sys.stdout.encoding
        sys.stdout.reconfigure(encoding=self.result_code) if args.type == 'html' else None
        self.alternative_language = args.alternative
        self.result_type = args.type
        self.target_language = ''
        self.query_string = ''
        self.result = ''

    def get_url(self, tl, qry, tk):
        url = f'https://{self.http_host}/translate_a/single?client=webapp&sl=auto&tl={tl}&hl=en&dt=at&dt=bd&dt=ex&' \
              f'dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=sos&dt=ss&dt=t&ssel=0&tsel=0&kc=1&tk={tk}&q={qry}'
        return url

    def get_synonym(self, resp):
        if resp[1]:
            self.result += '\n=========\n'
            self.result += f'0_0: Translations of {self.query_string}\n'
            for x in resp[1]:
                self.result += f'# {x[0][0]}.\n'
                for y in x[2]:
                    self.result += f'{y[0]}: {", ".join(y[1])}\n'

    def get_result(self, resp):
        for x in resp[0]:
            self.result += x[0] if x[0] else ''
        self.result += '\n'

    def get_definitions(self, resp):
        self.result += '\n=========\n'
        self.result += f'0_0: Definitions of {self.query_string}\n'
        for x in resp[12]:
            self.result += f'# {x[0] if x[0] else ""}.\n'
            for y in x[1]:
                self.result += f'  - {y[0]}\n'
                self.result += f'    * {y[2]}\n' if len(y) >= 3 else ''

    def get_examples(self, resp):
        self.result += '\n=========\n'
        self.result += f'0_0: Examples of {self.query_string}\n'
        for x in resp[13][0]:
            self.result += f'  * {x[0]}\n'

    def get_synonyms_en(self, resp):
        self.result += '\n=========\n'
        self.result += f'0_0: Synonyms of {self.query_string}\n'
        for idx, x in enumerate(resp[11]):
            self.result += f'# {x[0]}.\n'
            for y in x[1]:
                self.result += ', '.join(y[0]) + '\n'

    def get_resp(self, url):
        proxies = {
            'http': f'http://{self.http_proxy.strip() if self.http_proxy.strip() else "127.0.0.1:1080"}',
            'https': f'http://{self.http_proxy.strip() if self.http_proxy.strip() else "127.0.0.1:1080"}'
        }
        base_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
        session = requests.Session()
        session.headers = base_headers
        resp = session.get(url, proxies=proxies if self.http_proxy.strip() else None, timeout=5).json()
        return resp

    def result_to_html(self):
        css_text = """\
        <style type="text/css">
        p {white-space: pre-wrap;}
        pos {color: #0000FF;}
        example {color: #008080;}
        gray {color: #606060;}
        </style>"""
        self.result = re.sub(r'(#.*)', r'<pos><b>\1</b></pos>', self.result)
        self.result = re.sub(r'([*].*)', r'<example>\1</example>', self.result)
        self.result = re.sub(r'(0_0:.*?of)(.*)', r'<gray>\1</gray>\2', self.result)
        match = re.compile(rf"({re.escape('^_^')}: Translate)(.*)(To)(.*)")
        self.result = match.sub(r'<gray>\1</gray>\2<gray>\3</gray>\4', self.result)
        self.result = f'<html>\n<head>\n{css_text}\n</head>\n<body>\n<p>{self.result}</p>\n</body>\n</html>'

    async def get_translation(self, target_language, query_string, tkk=''):
        self.result = ''
        self.target_language = target_language
        self.query_string = query_string
        tk = Token(tkk).calculate_token(self.query_string)
        if len(self.query_string) > 5000:
            return '(╯‵□′)╯︵┻━┻: Maximum characters exceeded...'
        parse_query = urllib.parse.quote_plus(self.query_string)
        url = self.get_url(self.target_language, parse_query, tk)
        url_alt = self.get_url(self.alternative_language, parse_query, tk)
        try:
            loop = asyncio.get_running_loop()
            resp = loop.run_in_executor(None, partial(self.get_resp, url))
            resp_alt = loop.run_in_executor(None, partial(self.get_resp, url_alt))
            [resp, resp_alt] = await asyncio.gather(resp, resp_alt)
            if resp[2] == self.target_language:
                self.result += f'^_^: Translate {resp[2]} To {self.alternative_language}\n'
                self.get_result(resp)
                self.get_result(resp_alt)
                self.get_synonym(resp_alt)
            else:
                self.result += f'^_^: Translate {resp[2]} To {self.target_language}\n{self.query_string}\n'
                self.get_result(resp)
                self.get_synonym(resp)
            if self.synonyms_en and len(resp) >= 12 and resp[11]:
                self.get_synonyms_en(resp)
            if self.definitions_en and len(resp) >= 13 and resp[12]:
                self.get_definitions(resp)
            if self.examples_en and len(resp) >= 14 and resp[13]:
                self.get_examples(resp)
            if self.result_type == 'html':
                self.result_to_html()
            else:
                self.result = self.result.replace('<b>', '').replace('</b>', '')
            return self.result.encode(self.result_code, 'ignore').decode(self.result_code)
        except requests.exceptions.ReadTimeout:
            return '╰（‵□′）╯: ReadTimeout...'
        except requests.exceptions.ProxyError:
            return '(╯‵□′)╯︵┻━┻: ProxyError...'
        except Exception as e:
            return f'Errrrrrrrrror: {e}'


def get_args():
    h = 'translate.google.com'
    parser = argparse.ArgumentParser()
    parser.add_argument('target', type=str, default='en', help='target language (eg: zh-CN)')
    parser.add_argument('query', type=str, default='', help='query string')
    parser.add_argument('-s', dest='host', type=str, default='translate.google.com', help=f'host name (default: {h})')
    parser.add_argument('-p', dest='proxy', type=str, default='', help='proxy server (eg: 127.0.0.1:1080)')
    parser.add_argument('-a', dest='alternative', type=str, default='en', help='alternative language (default: en)')
    parser.add_argument('-r', dest='type', type=str, default='html', help='result type (default: html)')
    parser.add_argument('-m', dest='synonyms', type=bool, default=False, help='synonyms (default: False)')
    parser.add_argument('-d', dest='definitions', type=bool, default=True, help='definitions (default: True)')
    parser.add_argument('-e', dest='examples', type=bool, default=False, help='examples (default: False)')
    parser.add_argument('-k', dest='tkk', type=str, default='', help='tkk')
    return parser.parse_args()


def main(args=None):
    args = args if args else get_args()
    g_trans = GoogleTranslate(args)
    trans = asyncio.run(g_trans.get_translation(args.target, args.query, tkk=args.tkk))
    return trans


if __name__ == '__main__':
    print(main())
