#!/usr/bin/python
# -*- coding: utf-8 -*-

from YahooTWStock import YahooTWStock
import time
import os
import sys
from terminaltables import AsciiTable
from terminaltables import SingleTable

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

    stock_ids = ('2330', '2317', '2002', '1301', '2412', '2891', '0050', '0051', '0056', '00646')
    stock_ids_num = len(stock_ids)

    # Init table
    table_data = []
    table_data.append(['股票代號', '股票名稱', '股價'])
    for i in range(stock_ids_num):
        table_data.append(['', '', ''])

    #table = AsciiTable(table_data)
    table = SingleTable(table_data)

    # Creating a list of objects
    yahoo = []
    for stock_id in stock_ids:
        # Storing a list of object instances
        yahoo.append(YahooTWStock(stock_id))

    while (1):
        print('refresh...')
        for i in range(stock_ids_num):
            yahoo[i].refresh()
            #print('%6s | %s | %.2f' % (yahoo[i].get_id(), yahoo[i].get_name(), yahoo[i].get_price()))
            table.table_data[i+1][0] = yahoo[i].get_id()
            table.table_data[i+1][1] = yahoo[i].get_name()
            table.table_data[i+1][2] = yahoo[i].get_price()

        clearScreen()
        print(table.table)

        for i in range(5):
            print('wait %d sec to refresh...' % (5-i))
            time.sleep(1)
