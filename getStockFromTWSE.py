#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
# from tools import openURL

def getStockFromTWSE(id):
    _price = 0.0
    _name = ''

    # ref: http://wiki0918.pixnet.net/blog/post/222332253
    url = 'http://mis.tse.com.tw/stock/api/getStock.jsp?ch=%s.tw&json=1&_=' % id
    # openURL(url)
    r = requests.get(url)

    content = r.content
    # print(content)

    data = json.loads(content.decode('utf-8')) # load from json bytes
    #print(json.dumps(data, indent=4, sort_keys=True)) # pretty print json

    #print(data['msgArray'][0]['y']);

    _price = float(data['msgArray'][0]['y']) # 昨日收盤價, 不是當日股價
    _name = data['msgArray'][0]['ch']
    return _price, _name

def openURL(url):
    print(url)
    import webbrowser
    webbrowser.open(url)

if __name__ == '__main__':
    price, name = getStockFromTWSE(2330)
    print('name = %s, price = %.2f' % (name, price))
