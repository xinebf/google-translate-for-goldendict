#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ZHANG XINZENG
# Created on 2020-04-01 18:02


class Token:
    """
    https://www.52pojie.cn/thread-707169-1-1.html
    https://www.jianshu.com/p/af74f0719267
    """

    def __init__(self, tkk):
        self.tkk = tkk

    def calculate_token(self, text):
        if self.tkk == "":
            """
            422392.71207223
            406644.3293161072
            431767.4042228602
            440498.1287591069
            """
            self.tkk = "440498.1287591069"
        [first_seed, second_seed] = self.tkk.split(".")

        try:
            d = bytearray(text.encode('UTF-8'))
        except UnicodeDecodeError:
            d = bytearray(text)

        a = int(first_seed)
        for value in d:
            a += value
            a = self._work_token(a, "+-a^+6")
        a = self._work_token(a, "+-3^+b+-f")
        a ^= int(second_seed)
        if 0 > a:
            a = (a & 2147483647) + 2147483648
        a %= 1E6
        a = int(a)
        return str(a) + "." + str(a ^ int(first_seed))

    @staticmethod
    def _rshift(val, n):
        return val >> n if val >= 0 else (val + 0x100000000) >> n

    def _work_token(self, a, seed):
        for i in range(0, len(seed) - 2, 3):
            char = seed[i + 2]
            d = ord(char[0]) - 87 if char >= "a" else int(char)
            d = self._rshift(a, d) if seed[i + 1] == "+" else a << d
            a = a + d & 4294967295 if seed[i] == "+" else a ^ d
        return a
