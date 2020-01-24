#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : 张旭
# @Email   : zhangxu3486432@gmail.com
# @Blog    : https://zhangxu3486432.github.io
# @FileName: entrypoint.py
# @Time    : 2020/1/17

from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'cpd'])
