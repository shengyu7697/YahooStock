YahooStock
==========
YahooStock 是一個從 Yahoo 網站取得股票資訊的小工具， 分為 gui 版與 console 版。

Demo gui.  
![demo_gui](https://raw.github.com/shengyu7697/YahooStock/master/demo_gui.gif)  

Demo on ubuntu.  
![demo](https://raw.github.com/shengyu7697/YahooStock/master/demo.gif)  

## 特色
* 定時更新線上 stock 價格資訊  
* 使用 requests 取得網頁頁面  
* 可讀檔 / 存檔股票資訊 (使用 csv 格式)  

## 安裝相依套件
安裝必要的第三方套件
* PyQt5 (gui 版需要)
* requests
* terminaltables (console 版需要)
```
$ pip install requests
$ pip install terminaltables
```
或無腦安裝
```
pip3 install -r requirements.txt
```

## 如何使用
新增修改 stock.csv 裡的股票代號即可，接著執行 gui 版  
```
$ ./yahooStock-gui.py
```

或著 console 版  
```
$ ./yahooStock.py
```

## Todo
* 支援 BeautifulSoup 解析  
* 到價提醒， 設定價格以上通知/以下通知  
* 到價發送 email (Email class)  
* 平日 0900am - 1300pm 才做  

## 系統需求
* yahooStock.py => Python2 / 3
* yahooStock-gui.py => Python3

## 開發環境
* Python

## License
YahooStock is published under the MIT license.  
