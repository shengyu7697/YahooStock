#!/usr/bin/python
# -*- coding: utf-8 -*-
from getStockFromYahoo import getStockFromYahoo
# from getStockFromTWSE import getStockFromTWSE
import csv


class YahooTWStock(object):

    def __init__(self):
        self._id = []  # str
        self._price = []  # float
        self._name = []  # str
        self._size = 0

    def addStockId(self, stockId):
        self._id.append(stockId)  # str
        self._price.append(0.0)  # float
        self._name.append('')  # str
        self._size += 1

    def addStockIdList(self, stockIdList):
        for stockId in stockIdList:
            self._id.append(stockId)  # str
            self._price.append(0.0)  # float
            self._name.append('')  # str
            self._size += 1

    def remove(self, stockId):
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

    def loadFromStockCsv(self, filename):
        with open(filename) as csvfile:
            # rows = csv.reader(csvfile, delimiter=',')
            rows = csv.DictReader(csvfile, delimiter=',')

            # get column value
            for row in rows:
                self.addStockId(row['stock id'])

    def saveToStockCsv(self, filename):
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['stock id', 'stock name', 'price'])
            for i in range(self.size):
                writer.writerow([self.yahoo.id(i), self.yahoo.name(i), self.yahoo.price(i)])

    def _request(self, i):
        self._price[i], self._name[i] = getStockFromYahoo(self._id[i])
        # backup
        # self._price[i], self._name[i] = getStockFromTWSE(self._id[i])
