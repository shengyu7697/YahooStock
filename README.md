YahooStock
==========

## Introduction
Get stock information from yahoo.  

Demo on ubuntu.  
![demo](https://raw.github.com/shengyu7697/YahooStock/master/demo.gif)  

## Features
* 定時更新線上 stock 價格資訊  
* 使用 requests 取得網頁頁面  

## How to Use
change the stock_ids variable and execute.  
```
$ ./yahooStock.py
```

# Todo
* 支援 BeautifulSoup 解析  
* 從檔案讀取股票代號 (使用 csv 儲存格式)  
* 寫入 股票代號 股票名稱 價格 是否到價提醒 設定價格 以上通知/以下通知  
* 到價發送email (Email class)  
* 平日 0900am - 1300pm 才做  

## System Requirement
* 可以執行Python的系統

## Develop Environment
* Python

## License
YahooStock is published under the MIT license.  
