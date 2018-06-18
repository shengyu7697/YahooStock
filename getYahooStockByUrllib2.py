#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib # Python 2.x
#import http.client # Python 3.x
import urllib2
import re

def getYahooStockByUrllib2(id):
	httplib.HTTPConnection.debuglevel = 1

	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]

	# For finding stock price
	iRE_price = re.compile(r".*nowrap><b>([\d.]+)<.*", re.I | re.U | re.M | re.S)

	# For finding stock name
	# pattern: >2330台積電</a><br><a href="/pf/pfsel?stocklist=
	e = ".*>\d+" + r'(.+)</a><br><a href="/pf/pfsel\?stocklist=.*'
	debug_print(e, "for name")
	iRE_name = re.compile(e, re.I | re.U | re.M | re.S)

	# Get web page content
	content = opener.open('http://tw.stock.yahoo.com/q/q?s=%s' % id).read()

	# Print the whole content for debugging
	# print content

	match_price = iRE_price.match(content)
	if str(match_price) == 'None':
		print('Not found')

	match_name = iRE_name.match(content)
	if str(match_name) == 'None':
		print('Not found')

	_price = float(match_price.groups()[0])
	_name = unicode(match_name.groups()[0], "BIG5")
	return _price, _name

def debug_print(s, msg = None):
    #print "[DEBUG]", msg, s
    pass

if __name__ == '__main__':
	price, name = getYahooStockByUrllib2(2330)

	print(price)
	print(name)
