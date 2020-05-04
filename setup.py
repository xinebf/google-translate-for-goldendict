#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ZHANG XINZENG
# Created on 2020-05-03 19:31

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="google-translate-for-goldendict",
    version="1.3.1",
    author="xinebf",
    author_email="me@xinebf.com",
    description="Add Google translate to GoldenDict",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xinebf/google-translate-for-goldendict",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
