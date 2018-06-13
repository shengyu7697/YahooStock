#!/usr/bin/python
# -*- coding: utf-8 -*-

from yahooStock import YahooTWStock

if __name__ == '__main__':
    stock_ids = ('2330', '2891', '2317', '0050')

    #getStockInfo(stock_ids)

    for stock_id in stock_ids:
        yahoo = YahooTWStock(stock_id)
        print "%s\t%s\t%.2f" % (yahoo.get_id(), yahoo.get_name(), yahoo.get_price())
    
    #raw_input( "Press any key..." )
