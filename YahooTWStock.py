#!/usr/bin/python
# -*- coding: utf-8 -*-
from getYahooStockByRequests import getYahooStockByRequests

class YahooTWStock(object):
    def __init__(self, stock_id):
        self._id = stock_id
        self._price = 0.0
        self._name = ''
        #self.refresh() # refresh too slow, so call it later.

    def refresh(self):
        self._request()

    def get_id(self):
        return self._id

    def get_price(self):
        return self._price

    def get_name(self):
        return self._name

    def _request(self):
        self._price, self._name = getYahooStockByRequests(self._id)
