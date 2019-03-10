#!/usr/bin/env python3

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QDialogButtonBox,
        QLabel, QPushButton, QTableWidget, QTableWidgetItem,
        QVBoxLayout, QWidget, QHeaderView)
from ui.gui import Ui_MainWindow
from YahooTWStock import YahooTWStock
import csv

class Worker(QtCore.QThread):
    signalDataChanged = QtCore.pyqtSignal(int, str, str, float) # 信號
    notifyProgress = QtCore.pyqtSignal(int)

    def __init__(self, yahoo, parent=None):
        super(self.__class__, self).__init__(parent)
        self.yahoo = yahoo

    def stop(self):
        self.working = False

    def run(self):
        self.working = True
        while self.working:
            for i in range(len(self.yahoo)):
                print(i)
                self.yahoo[i].refresh()
                print('%6s | %s | %.2f' % (self.yahoo[i].id, self.yahoo[i].name, self.yahoo[i].price))
                if (self.working):
                    self.signalDataChanged.emit(i, self.yahoo[i].id, self.yahoo[i].name, self.yahoo[i].price)  # 發送信號
                    self.notifyProgress.emit(i)
                else:
                    break
            #self.sleep(1)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setRange(0, 100)
        self.statusBar().addPermanentWidget(self.progressBar)
        self.statusBar().setSizeGripEnabled(False)
        self.statusBar().setStyleSheet("QStatusBar::item {border: none;}")

        self.setWindowTitle("YahooStock")
        self.move(100, 100)
        self.show()

        stock_ids = self.loadStockCsv('stock.csv')
        #stock_ids = ['2330', '2317', '2002', '1301', '2412', '2891', '0050', '0051', '0056', '00646']

        self.yahoo = []
        for stock_id in stock_ids:
            # Storing a list of object instances
            self.yahoo.append(YahooTWStock(stock_id))

        self.work = Worker(self.yahoo)
        self.work.signalDataChanged.connect(self.updateStock)
        self.work.notifyProgress.connect(self.onProgress)

        self.initTable()

        self.setMenuAction()
        self.setConnections()

        self.ui.statusbar.showMessage('Press start to update', 5000)

    def loadStockCsv(self, fname):
        with open(fname, newline='') as csvfile:
            #rows = csv.reader(csvfile, delimiter=',')
            rows = csv.DictReader(csvfile, delimiter=',')

            # get column value
            stockIdList = []
            for row in rows:
                stockIdList.append(row['stock id'])
            #print(stockIdList)
        return stockIdList

    def setMenuAction(self):
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionLicense.triggered.connect(self.showLicense)
        self.ui.actionAbout.triggered.connect(self.showAbout)

    def showLicense(self):
        QtWidgets.QMessageBox.information(self, 'License', '')

    def showAbout(self):
        QtWidgets.QMessageBox.information(self, 'About', '')

    def setConnections(self):
        self.ui.pushButtonStart.clicked.connect(self.start)
        self.ui.pushButtonStop.clicked.connect(self.stop)
        self.ui.pushButtonExit.clicked.connect(self.close)
        self.ui.pushButtonAdd.clicked.connect(self.add)

    def start(self):
        print('start')
        self.ui.statusbar.showMessage('Start', 2000)
        self.work.start()

    def stop(self):
        print('stop')
        self.ui.statusbar.showMessage('Stop', 2000)
        self.work.stop()

    def add(self):
        print('add')
        self.ui.statusbar.showMessage('Add', 2000)
        self.appendDataAndTable()

    def initTable(self):
        self.table = self.ui.tableWidget

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['股票代號', '股票名稱', '股價'])

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)  # 列寬設置
        #self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # 列寬設置
        self.table.horizontalHeader().setStretchLastSection(True) # 充滿列寬
        #self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch) # 行高設置
        #self.table.verticalHeader().setStretchLastSection(True) # 充滿行高

        self.table.setSelectionBehavior(QTableWidget.SelectRows) # 行選擇模式
        self.table.setSelectionMode(QAbstractItemView.SingleSelection); # 無法拖拽選擇

        self.data = {'股票代號' : [], '股票名稱' : [], '股價' : []}
        for i in range(len(self.yahoo)):
            self.data['股票代號'].append(str(self.yahoo[i].id))
            self.data['股票名稱'].append(str('none'))
            self.data['股價'].append(str('0'))

        self.insertTable()

    def insertTable(self):
        self.table.setRowCount(0)
        for i in range(len(self.yahoo)):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(self.data['股票代號'][i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.data['股票名稱'][i])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.data['股價'][i])))

    def appendDataAndTable(self):
        stock_id = self.ui.lineEdit.text()
        name = 'none'
        price = 0

        # appendData
        self.data['股票代號'].append(str(stock_id))
        self.data['股票名稱'].append(str(name))
        self.data['股價'].append(str(price))

        # appendTable
        i = self.table.rowCount()
        self.table.insertRow(i)
        self.table.setItem(i, 0, QTableWidgetItem(str(self.data['股票代號'][i])))
        self.table.setItem(i, 1, QTableWidgetItem(str(self.data['股票名稱'][i])))
        self.table.setItem(i, 2, QTableWidgetItem(str(self.data['股價'][i])))

        # update stock to self.yahoo list
        self.yahoo.append(YahooTWStock(stock_id))

    def updateTable(self, i):
        print('updateTable')
        self.table.setItem(i, 0, QTableWidgetItem(str(self.data['股票代號'][i])))
        self.table.setItem(i, 1, QTableWidgetItem(str(self.data['股票名稱'][i])))
        self.table.setItem(i, 2, QTableWidgetItem(str(self.data['股價'][i])))

    def updateData(self, i, id, name, price):
        print('updateData')
        self.data['股票代號'][i] = id
        self.data['股票名稱'][i] = name
        self.data['股價'][i] = price

    def updateStock(self, i, id, name, price):
        print('updateStock %d %s %s %f' % (i, id, name, price))
        self.ui.statusbar.showMessage('Update %d/%d...' % (i+1, len(self.yahoo)), 2000)
        self.updateData(i, id, name, price)
        self.updateTable(i)

    def onProgress(self, i):
        self.progressBar.setValue(100 * (i + 1) / len(self.yahoo))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec_())
