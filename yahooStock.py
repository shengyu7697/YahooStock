#!/usr/bin/python
# -*- coding: utf-8 -*-

from YahooTWStock import YahooTWStock
import time
import os
import sys
# from terminaltables import AsciiTable
from terminaltables import SingleTable


class StockTable():

    def __init__(self, parent=None):
        self.load()
        pass

    def load(self):
        # stock_ids = loadFromStockCsv('stock.csv')
        stock_ids = ['2330', '2317', '2002', '1301', '2412', '2891', '0050', '0051', '0056', '00646']

        self.yahoo = YahooTWStock()
        for stock_id in stock_ids:
            # Storing a list of object instances
            self.yahoo.add(stock_id)

        self.initDataAndTable()

    def initDataAndTable(self):
        self.data = []
        self.data.append(['股票代號', '股票名稱', '股價'])
        for i in range(self.yahoo.size):
            self.data.append([str(self.yahoo.id(i)), 'none', '0'])

        # self.table = AsciiTable(self.data)
        self.table = SingleTable(self.data)

    def updateTable(self, i):
        self.table.table_data[i + 1][0] = str(self.data[i + 1][0])
        self.table.table_data[i + 1][1] = str(self.data[i + 1][1])
        self.table.table_data[i + 1][2] = str(self.data[i + 1][2])
        pass

    def updateData(self, i, id, name, price):
        self.data[i + 1][0] = id
        self.data[i + 1][1] = name
        self.data[i + 1][2] = price

    def updateStock(self, i, id, name, price):
        # print('updateStock %d %s %s %f' % (i, id, name, price))
        self.updateData(i, id, name, price)
        self.updateTable(i)

    def refresh(self):
        self.run()

    def run(self):
        for i in range(self.yahoo.size):
            self.yahoo.refresh(i)
            # print('%6s | %s | %.2f' % (yahoo.id(i), yahoo[i].name, yahoo[i].price))
            self.updateStock(i, self.yahoo.id(i), self.yahoo.name(i), self.yahoo.price(i))

    def showTable(self):
        print(self.table.table)

def clearScreen():
    # print('\n' * 80)  # prints 80 line breaks, Faking Clear Screen (for PyCharm)
    if os.name == 'nt':
        os.system('cls')  # on windows
    else:
        os.system('clear')  # on linux / os x

if __name__ == '__main__':
    if sys.version[0] == '2':
        reload(sys)
        sys.setdefaultencoding('utf8')

    stockTable = StockTable()
    stockTable.showTable()

    while (1):
        print('refresh...')
        stockTable.refresh()

        clearScreen()
        stockTable.showTable()

        for i in range(5):
            print('wait %d sec to refresh...' % (5-i))
            time.sleep(1)
