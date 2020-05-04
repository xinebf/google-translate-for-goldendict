# google-translate-for-goldendict
Add Google translate for GoldenDict

[GoldenDict][1] 是一个非常好用的词典工具, 却不能整句或整段的翻译, 时常需要借助 [Google translate][2] 对于将 Google 翻译加到 GoldenDict 是一个很好的方法 φ(゜▽゜*)♪

![screenshot](https://raw.githubusercontent.com/xinebf/google-translate-for-goldendict/master/screenshot.png)

**使用方法:**

需要 python 3.7+ 并安装 requests:

`pip3 install requests`

GoldenDict - 编辑 - 字典 - 字典来源 - 程式

类型: `Html`

名称: `Google Translate`

命令行: `python H:\PathTo\googletranslate.py zh-CN %GDWORD%`

图示: `H:\PathTo\google_translate.png`

**Tips**

默认设置不能使用的可以尝试将 `http_host` 设为: `translate.google.cn`.

```
python H:\PathTo\googletranslate.py zh-CN %GDWORD% -s "translate.google.cn"
```

类型可以设为 `Html` 或 `纯文本`.

其中: `Html` 对应 `-r "html"`. `纯文本` 对应 `-r "plain"`

```
positional arguments:
  target          target language (eg: zh-CN)
  query           query string

optional arguments:
  -h, --help      show this help message and exit
  -s HOST         host name (default: translate.google.com)
  -p PROXY        proxy server (eg: 127.0.0.1:1080)
  -a ALTERNATIVE  alternative language (default: en)
  -r TYPE         result type (default: html)
  -m SYNONYMS     synonyms (default: False)
  -d DEFINITIONS  definitions (default: True)
  -e EXAMPLES     examples (default: False)
  -k TKK          tkk
```

[1]: https://github.com/goldendict/goldendict
[2]: https://translate.google.com/
