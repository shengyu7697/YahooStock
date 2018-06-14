#!/usr/bin/python
# -*- coding: utf-8 -*-
from yahooStockByUrllib2 import getYahooStockByUrllib2
from yahooStockByRequests import getYahooStockByRequests

class YahooTWStock(object):
    def __init__(self, stock_id):
        self._id = stock_id
        self._price = 0.0
        self._name = ''
        #self.refresh() # refresh too slow, so call it later.

    def refresh(self):
        #self._requestByUrllib2() # urllib2 slower than requests
        self._requestByRequests()

    def get_id(self):
        return self._id

    def get_price(self):
        return self._price

    def get_name(self):
        return self._name

    def _requestByUrllib2(self):
        self._price, self._name = getYahooStockByUrllib2(self._id)

    def _requestByRequests(self):
        self._price, self._name = getYahooStockByRequests(self._id)
