#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import chardet
# from tools import openURL, writeToFile

def getStockFromYahoo(id):
    _price = 0.0
    _name = ''

    url = 'http://tw.stock.yahoo.com/q/q?s=%s' % id
    # openURL(url)
    r = requests.get(url)
    content = r.content

    # 根據傳進來的參數自動辨別編碼格式，然後進行相應的解碼
    encode_type = chardet.detect(content)
    content = content.decode(encode_type['encoding'])

    # For finding stock price
    iRE_price = re.compile(r'.*nowrap><b>([\d.]+)<.*', re.I | re.U | re.M | re.S)

    # For finding stock name
    # pattern: >2330台積電</a><br><a href="/pf/pfsel?stocklist=
    e = '.*>\d+' + r'(.+)</a><br><a href="/pf/pfsel\?stocklist=.*'
    #debug_print(e)
    iRE_name = re.compile(e, re.I | re.U | re.M | re.S)

    # Print the whole content for debugging
    # print(content)
    # writeToFile(content)

    match_price = iRE_price.match(content)
    # print('match_price =', match_price)
    if str(match_price) == 'None':
        print('Not found')
        return -1, None  # 早上還沒開盤前會找不到

    match_name = iRE_name.match(content)
    if str(match_name) == 'None':
        print('Not found')
        return -1, None

    _price = float(match_price.groups()[0])
    _name = match_name.groups()[0]
    return _price, _name

def debug_print(msg):
    tag = 'DEBUG'
    print('[%s] %s' % (tag, msg))

if __name__ == '__main__':
    price, name = getStockFromYahoo(2330)
    print('name = %s, price = %.2f' % (name, price))
