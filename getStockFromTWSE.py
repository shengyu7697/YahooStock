#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json

def getStockFromTWSE(id):
	# ref: http://wiki0918.pixnet.net/blog/post/222332253
	r = requests.get('http://mis.tse.com.tw/stock/api/getStock.jsp?ch=%s.tw&json=1&_=' % id)
	content = r.content

	data = json.loads(content) # load from json string
	#print(json.dumps(data, indent=4, sort_keys=True)) # pretty print json

	#print(data['msgArray'][0]['y']);

	_price = data['msgArray'][0]['y'] # 昨日收盤價, 不是當日股價
	_name = data['msgArray'][0]['ch']
	return _price, _name

if __name__ == '__main__':
	price, name = getStockFromTWSE(2330)

	print(price)
	print(name)
