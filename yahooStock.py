#!/usr/bin/python
# -*- coding: utf-8 -*-
import httplib
import urllib2
import re

class YahooTWStock(object):
    def __init__(self, stock_id):
        self._id = stock_id
        self._price = 0.0
        self._name = ''
        self.refresh()

    def refresh(self):
        self._request()

    def get_id(self):
        return self._id

    def get_price(self):
        return self._price

    def get_name(self):
        return self._name

    def _request(self):
        httplib.HTTPConnection.debuglevel = 1

        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]

        # For finding stock price
        iRE_price = re.compile(r".*nowrap><b>([\d.]+)<.*", re.I | re.U | re.M | re.S)

        # For finding stock name
        # pattern: >2330台積電</a><br><a href="/pf/pfsel?stocklist=
        e = ".*>\d+" + r'(.+)</a><br><a href="/pf/pfsel\?stocklist=.*'
        debug_print( e, "for name" )
        iRE_name = re.compile(e, re.I | re.U | re.M | re.S)

        # Get web page content
        content = opener.open('http://tw.stock.yahoo.com/q/q?s=' + self._id).read()

        # Print the whole content for debugging
        #print content

        match_price = iRE_price.match(content)
        if str(match_price) == 'None':
            print 'Not found'

        match_name = iRE_name.match(content)
        if str(match_name) == 'None':
            print 'Not found'

        self._price = float(match_price.groups()[0])
        self._name = unicode(match_name.groups()[0], "BIG5")

def debug_print( s, msg = None ):
    #print "[DEBUG]", msg, s
    pass

def getStockInfo(stock_ids):
    httplib.HTTPConnection.debuglevel = 1

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    # For finding stock price
    iRE_price = re.compile(r".*nowrap><b>([\d.]+)<.*", re.I | re.U | re.M | re.S)

    # For finding stock name
    # pattern: >2330台積電</a><br><a href="/pf/pfsel?stocklist=
    e = ".*>\d+" + r'(.+)</a><br><a href="/pf/pfsel\?stocklist=.*'
    debug_print( e, "for name" )
    iRE_name = re.compile(e, re.I | re.U | re.M | re.S)

    for stock_id in stock_ids:
        # Get web page content
        content = opener.open('http://tw.stock.yahoo.com/q/q?s=' + stock_id).read()

        # Print the whole content for debugging
        #print content

        match_price = iRE_price.match(content)
        if str(match_price) == 'None':
            print 'Not found, continue ... '
            continue

        match_name = iRE_name.match(content)
        if str(match_name) == 'None':
            print 'Not found, continue ... '
            continue

        stock_price = match_price.groups()[0]
        stock_name = unicode(match_name.groups()[0], "BIG5")

        # Print result
        print "%s\t%s\t%.2f" % (stock_id, stock_name, float(stock_price))

if __name__ == '__main__':
    stock_ids = ('2330', '2891', '2317', '0050')

    #getStockInfo(stock_ids)

    for stock_id in stock_ids:
        yahoo = YahooTWStock(stock_id)
        print "%s\t%s\t%.2f" % (yahoo.get_id(), yahoo.get_name(), yahoo.get_price())
    
    #raw_input( "Press any key..." )
