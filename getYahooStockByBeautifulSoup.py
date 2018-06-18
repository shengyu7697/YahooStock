#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import webbrowser
import sys

def parseHtml(content):
	title = content.get('title')
	url = content.get('href')
	#style = content.get('style')
	#style = content.find('url').getText()
	#print title
	#print url
	return url

def parseYahooPage(id1):
	r = requests.get("http://tw.stock.yahoo.com/q/q?s=%s" % id1)
	c = r.content

	#soup = BeautifulSoup(c, "html.parser")
	soup = BeautifulSoup(c, "lxml")
	#print(soup.prettify())

	table = soup.find_all("table")[1].find_all("b")
	print(table)
	#print "found %d links" % len(links)

if __name__ == '__main__':
	parseYahooPage(2330)
