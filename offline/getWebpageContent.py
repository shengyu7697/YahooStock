#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

content = opener.open( 'http://tw.stock.yahoo.com/q/q?s=' + '0050').read()
print content
