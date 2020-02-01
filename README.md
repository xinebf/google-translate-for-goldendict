# google-translate-for-goldendict
Add Google translate for GoldenDict

[GoldenDict][1] 是一个非常好用的词典工具, 却不能整句或整段的翻译, 时常需要借助 [Google translate][2] 对于将 Google 翻译加到 GoldenDict 是一个很好的方法 φ(゜▽゜*)♪

![screenshot](https://raw.githubusercontent.com/xinebf/google-translate-for-goldendict/master/screenshot.png)

**使用方法:**

需要 python3.7+ 并安装 requests:

`pip3 install requests`

GoldenDict - 编辑 - 字典 - 字典来源 - 程式

类型: `纯文字`

名称: `Google Translate`

命令行: `python H:\PathTo\googletranslate.py zh-CN %GDWORD%`

图示: `H:\PathTo\google_translate.png`

**Tips**

默认设置不能使用的可以尝试将 `http_host` 设为: `translate.google.cn`.

类型可以设为 `Html`, 并同时将 `result_type` 设为: `html`.

[1]: https://github.com/goldendict/goldendict
[2]: https://translate.google.com/
