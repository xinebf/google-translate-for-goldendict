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
from googletranslatetk import Token


class GoogleTranslate(object):
    def __init__(self, http_host='translate.googleapis.com', http_proxy='', synonyms_en=False, definitions_en=True,
                 examples_en=False, result_code=sys.stdout.encoding, alternative_language='en', result_type='plain'):
        self.http_host = http_host
        self.http_proxy = http_proxy
        self.synonyms_en = synonyms_en
        self.definitions_en = definitions_en
        self.examples_en = examples_en
        self.result_code = 'utf-8' if result_type == 'html' else result_code
        sys.stdout.reconfigure(encoding=self.result_code) if result_type == 'html' else None
        self.alternative_language = alternative_language
        self.result_type = result_type
        self.target_language = ''
        self.query_string = ''
        self.result = ''

    def get_url(self, tl, qry, tk):
        url = f'https://{self.http_host}/translate_a/single?client=gtx&sl=auto&tl={tl}&dt=at&dt=bd&dt=ex&' \
              f'dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&tk={tk}&q={qry}'
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

    async def get_translation(self, target_language, query_string, tkk=None):
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
                self.result = self.result.replace("<b>", "").replace("</b>", "")
            return self.result.encode(self.result_code, 'ignore').decode(self.result_code)
        except requests.exceptions.ReadTimeout:
            return '╰（‵□′）╯: ReadTimeout...'
        except requests.exceptions.ProxyError:
            return '(╯‵□′)╯︵┻━┻: ProxyError...'
        except Exception as e:
            return f'Errrrrrrrrror {e}'


if __name__ == '__main__':
    gtrans = GoogleTranslate(result_type='html')
    print(asyncio.run(gtrans.get_translation(target_language=sys.argv[1], query_string=sys.argv[2], tkk=None)))
