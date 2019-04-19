#!/usr/bin/env python3

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QDialogButtonBox,
        QLabel, QPushButton, QTableWidget, QTableWidgetItem,
        QVBoxLayout, QWidget, QHeaderView, QDialog)
from ui.gui import Ui_MainWindow
from ui.license import Ui_Dialog
from YahooTWStock import YahooTWStock
import csv
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

VERSION = '1.0.0'

class Worker(QtCore.QThread):
    signalDataChanged = QtCore.pyqtSignal(int, str, str, float) # 信號
    notifyProgress = QtCore.pyqtSignal(int)

    def __init__(self, yahoo, parent=None):
        super(self.__class__, self).__init__(parent)
        self.yahoo = yahoo
        self.progress = 0

    def stop(self):
        self.working = False

    def task(self, i):
        self.yahoo[i].refresh()
        print('%6s | %s | %.2f' % (self.yahoo[i].id, self.yahoo[i].name, self.yahoo[i].price))
        return i

    def callback(self, future):
        i = future.result()
        print(i)

        self.signalDataChanged.emit(i, self.yahoo[i].id, self.yahoo[i].name, self.yahoo[i].price)  # 發送信號

        self.progress += 100 / len(self.yahoo)
        self.notifyProgress.emit(self.progress)

    def run(self):
        self.working = True
        while self.working:
            self.progress = 0

            #executor = ThreadPoolExecutor(max_workers=5)
            #for i in range(len(self.yahoo)):
            #    future = executor.submit(self.task, i)
            #    future.add_done_callback(self.callback)
            #executor.shutdown(wait=True)

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futureList = []
                for i in range(len(self.yahoo)):
                    future = executor.submit(self.task, i)
                    future.add_done_callback(self.callback)
                    futureList.append(future)

                for future in concurrent.futures.as_completed(futureList):
                    try:
                        data = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (future, exc))
                    else:
                        print('%r index = %d' % (future, data))

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

        self.load()

        self.setMenuAction()
        self.setConnections()

        self.ui.statusbar.showMessage('Press start to update', 5000)
        self.ui.pushButtonStart.setEnabled(True)
        self.ui.pushButtonStop.setEnabled(False)

    def loadFromStockCsv(self, fname):
        with open(fname, newline='') as csvfile:
            #rows = csv.reader(csvfile, delimiter=',')
            rows = csv.DictReader(csvfile, delimiter=',')

            # get column value
            stockIdList = []
            for row in rows:
                stockIdList.append(row['stock id'])
            #print(stockIdList)
        return stockIdList

    def saveToStockCsv(self, fname):
        with open(fname, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['stock id', 'stock name', 'price'])
            for i in range(len(self.yahoo)):
                writer.writerow([self.yahoo[i].id, self.yahoo[i].name, self.yahoo[i].price])

    def setMenuAction(self):
        self.ui.actionLoad.triggered.connect(self.load)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionLicense.triggered.connect(self.showLicense)
        self.ui.actionAbout.triggered.connect(self.showAbout)

    def showLicense(self):
        licenseDialog = QDialog(self)
        uiDialog = Ui_Dialog()
        uiDialog.setupUi(licenseDialog)
        uiDialog.ExitButton.clicked.connect(licenseDialog.close)
        licenseDialog.show()

    def showAbout(self):
        QtWidgets.QMessageBox.information(self, 'About', 'YahooStock ' + VERSION + '\n'
                                          'Author: ShengYu')

    def setConnections(self):
        self.ui.pushButtonStart.clicked.connect(self.start)
        self.ui.pushButtonStop.clicked.connect(self.stop)
        self.ui.pushButtonExit.clicked.connect(self.close)
        self.ui.pushButtonAdd.clicked.connect(self.add)

    def load(self):
        print('load')
        self.ui.statusbar.showMessage('Load', 2000)

        stock_ids = self.loadFromStockCsv('stock.csv')
        #stock_ids = ['2330', '2317', '2002', '1301', '2412', '2891', '0050', '0051', '0056', '00646']

        self.yahoo = []
        for stock_id in stock_ids:
            # Storing a list of object instances
            self.yahoo.append(YahooTWStock(stock_id))

        self.work = Worker(self.yahoo)
        self.work.signalDataChanged.connect(self.updateStock)
        self.work.notifyProgress.connect(self.onProgress)

        self.initDataAndTable()
        self.ui.statusbar.showMessage('Load done.', 2000)

    def save(self):
        print('save')
        self.ui.statusbar.showMessage('Save', 2000)

        self.saveToStockCsv('stock.csv')
        self.ui.statusbar.showMessage('Save done.', 2000)

    def start(self):
        self.ui.pushButtonStart.setEnabled(False)
        self.ui.pushButtonStop.setEnabled(True)
        print('start')
        self.ui.statusbar.showMessage('Start', 2000)
        self.work.start()

    def stop(self):
        self.ui.pushButtonStart.setEnabled(True)
        self.ui.pushButtonStop.setEnabled(False)
        print('stop')
        self.ui.statusbar.showMessage('Stop', 2000)
        self.work.stop()

    def add(self):
        print('add')
        self.ui.statusbar.showMessage('Add', 2000)
        self.appendDataAndTable()

    def initDataAndTable(self):
        # initTable
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

        # initData
        self.data = {'股票代號' : [], '股票名稱' : [], '股價' : []}
        for i in range(len(self.yahoo)):
            self.data['股票代號'].append(str(self.yahoo[i].id))
            self.data['股票名稱'].append(str('none'))
            self.data['股價'].append(str('0'))

        # insertTable
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

    def onProgress(self, value):
        self.progressBar.setValue(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec_())
