#!/usr/bin/python
# -*- coding: utf-8 -*-

from YahooTWStock import YahooTWStock
import time
import os

def clearScreen():
    # print('\n' * 80)  # prints 80 line breaks, Faking Clear Screen (for PyCharm)
    if os.name == 'nt':
        os.system('cls')  # on windows
    else:
        os.system('clear')  # on linux / os x

if __name__ == '__main__':
    stock_ids = ('2330', '2317', '2891', '0050', '0056')

    #getStockInfo(stock_ids)

    # Creating a list of objects
    yahoo = []
    for stock_id in stock_ids:
        # Storing a list of object instances
        yahoo.append(YahooTWStock(stock_id))

    while (1):
        for i in range(len(stock_ids)):
            yahoo[i].refresh()
            print("%s\t%s\t%.2f") % (yahoo[i].get_id(), yahoo[i].get_name(), yahoo[i].get_price())

        print("wait 5 sec to refresh...")
        time.sleep(5)

        clearScreen()


    #raw_input( "Press any key..." )
