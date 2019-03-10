#!/usr/bin/python
# -*- coding: utf-8 -*-
from getStockFromYahoo import getStockFromYahoo

class YahooTWStock(object):
    def __init__(self, stock_id):
        self._id = stock_id # str
        self._price = 0.0 # float
        self._name = '' # str
        #self.refresh() # refresh too slow, so call it later.

    def refresh(self):
        self._request()

    @property
    def id(self):
        return self._id

    @property
    def price(self):
        return self._price

    @property
    def name(self):
        return self._name

    def _request(self):
        self._price, self._name = getStockFromYahoo(self._id)
