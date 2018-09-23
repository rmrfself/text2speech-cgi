#!D:\Python25\python.exe -u
# -*- coding: utf-8 -*-

import pyquery

import sys
print sys.getdefaultencoding()

print pyquery.PyQuery(url='http://dict.youdao.com/search?q=speech').text().encode('utf8')
