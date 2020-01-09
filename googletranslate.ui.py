#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ZHANG XINZENG
# Created on 2020-01-09 20:31

import asyncio
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import threading as td
from queue import Queue

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

        self.run_queue = Queue()
        self.trans_button = ttk.Button(frm_input, text='trans', width=6, command=self.run)
        self.trans_button.pack(anchor=tk.NE, side=tk.LEFT)

        self.st = scrolledtext.ScrolledText(frm_output, state=tk.NORMAL)
        self.st.insert(tk.END, 'Google Translate\n')
        self.st.pack(anchor=tk.NW, fill=tk.BOTH, expand=1)

        self.input_entry.bind('<Return>', self.run)
        self.input_entry.bind('<Escape>', lambda event=None: self.input_text.set(''))

    def run(self, event=None):
        if self.run_queue.empty():
            td.Thread(target=self.trans).start()

    def trans(self):
        gui_style = ttk.Style()
        gui_style.configure('Ui.TButton', foreground='#FF0000')
        self.trans_button.config(style='Ui.TButton')
        self.run_queue.put(1)
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
        self.run_queue.get()
        gui_style.configure('Ui.TButton', foreground='#000000')


if __name__ == '__main__':
    app = tk.Tk()
    UITranslate(app)
    app.mainloop()
