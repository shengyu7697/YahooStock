#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re

def getYahooStockByRequests(id):
	r = requests.get("http://tw.stock.yahoo.com/q/q?s=%s" % id)
	content = r.content

	# For finding stock price
	iRE_price = re.compile(r".*nowrap><b>([\d.]+)<.*", re.I | re.U | re.M | re.S)

	# For finding stock name
	e = ".*>\d+" + r'(.+)</a><br><a href="/pf/pfsel\?stocklist=.*'
	iRE_name = re.compile(e, re.I | re.U | re.M | re.S)

	match_price = iRE_price.match(content)
	if str(match_price) == 'None':
		print('Not found')

	match_name = iRE_name.match(content)
	if str(match_name) == 'None':
		print('Not found')

	_price = float(match_price.groups()[0])
	_name = unicode(match_name.groups()[0], "BIG5")
	return _price, _name

if __name__ == '__main__':
	price, name = getYahooStockByRequests(2330)

	print(price)
	print(name)
