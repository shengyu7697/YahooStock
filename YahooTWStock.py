#!/usr/bin/python
# -*- coding: utf-8 -*-
from getStockFromYahoo import getStockFromYahoo
# from getStockFromTWSE import getStockFromTWSE


class YahooTWStock(object):

    def __init__(self):
        self._id = []  # str
        self._price = []  # float
        self._name = []  # str
        self._size = 0

    def add(self, stock_id):
        self._id.append(stock_id)  # str
        self._price.append(0.0)  # float
        self._name.append('')  # str
        self._size += 1

    def remove(self, stock_id):
        # TODO
        pass

    def refresh(self, i):
        self._request(i)

    def id(self, i):
        return self._id[i]

    def price(self, i):
        return self._price[i]

    def name(self, i):
        return self._name[i]

    @property
    def size(self):
        return self._size

    def _request(self, i):
        self._price[i], self._name[i] = getStockFromYahoo(self._id[i])
        # backup
        # self._price[i], self._name[i] = getStockFromTWSE(self._id[i])
