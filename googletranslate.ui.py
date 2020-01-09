#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ZHANG XINZENG
# Created on 2020-01-09 20:31

import asyncio
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

from googletranslate import GoogleTranslate


class UITranslate(GoogleTranslate):
    def __init__(self, window):
        super().__init__(result_code='utf-8', synonyms_en=True, definitions_en=True, examples_en=True)
        self.window = window
        self.window.title('Google Translate')

        frm = tk.Frame(self.window)
        frm.pack(anchor=tk.NW, fill=tk.BOTH, expand=1)

        frm_input = tk.Frame(frm)
        frm_output = tk.Frame(frm)
        frm_input.pack(anchor=tk.NW, fill=tk.X)
        frm_output.pack(anchor=tk.NW, fill=tk.BOTH, expand=1)

        self.input_text = tk.StringVar()
        self.input_entry = ttk.Entry(frm_input, textvariable=self.input_text)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.trans_button = ttk.Button(frm_input, text='trans', width=6, command=self.trans)
        self.trans_button.pack(anchor=tk.NE, side=tk.LEFT)

        self.st = scrolledtext.ScrolledText(frm_output, state=tk.NORMAL)
        self.st.insert(tk.END, 'Google Translate\n')
        self.st.pack(anchor=tk.NW, fill=tk.BOTH, expand=1)

        self.input_entry.bind('<Return>', self.trans)
        self.input_entry.bind('<Escape>', lambda event=None: self.input_text.set(''))

    def trans(self, event=None):
        if self.input_text.get():
            query_string = self.input_text.get()
        else:
            try:
                query_string = self.window.clipboard_get()
                self.window.clipboard_clear()
            except Exception as e:
                query_string = str(e)
        asyncio.run(self.get_translation(target_language='zh-CN', query_string=query_string))
        self.st.delete('1.0', tk.END)
        self.st.insert(tk.END, self.result)


if __name__ == '__main__':
    app = tk.Tk()
    UITranslate(app)
    app.mainloop()
