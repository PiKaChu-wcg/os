from page import page
from information import Information as info
import pandas as pd
import numpy as np
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qdarkstyle import load_stylesheet_pyqt5


class QtTable(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]


class mywin(QMainWindow):
    def __init__(self, shape):
        super().__init__()
        self.shape = shape
        self.info = info()
        self.initUI(shape)

    def initUI(self, shape):
        self.setGeometry(300, 300, *shape)
        # 数据显示的组件
        self.pagelist = page()
        self.view = QTableView(self)
        self.view.setGeometry(0, 33, shape[0] * 0.5, shape[1] - 33)
        self.view.setModel(QtTable(self.pagelist.list))
        # 菜单项
        menubar = self.menuBar()
        dataMenu = menubar.addMenu('&Data')
        impAct = QAction('Import', self)
        expAct = QAction('Export', self)
        impAct.triggered.connect(self.importdata)
        expAct.triggered.connect(self.exportdata)
        dataMenu.addAction(impAct)
        dataMenu.addAction(expAct)
        # 下拉框,选择算法
        algselector = QComboBox(self)
        algselector.setGeometry(shape[0] * 0.5 + 20, 50, 150, 20)
        algselector.addItems(['先入先出', '最近最久未使用'])
        algselector.currentIndexChanged[int].connect(self.changealg)
        # 填入内存地址
        self.qle1 = QLineEdit(self)
        self.qle1.move(shape[0] * 0.5 + 20, 140)
        self.qle1.resize(150, 30)
        self.qle1.setPlaceholderText("内存地址")
        # 按钮
        self.btn1 = QPushButton("调用内存", self)
        self.btn1.move(shape[0] * 0.5 + 20, 240)
        self.btn1.clicked.connect(self.query)
        # 缺页率显示
        self.lb1 = QLabel(self)
        self.lb1.setText("缺页率:0/0  0%")
        self.lb1.move(shape[0] * 0.5 + 20, 340)
        self.lb1.resize(150, 30)
        # 默认页长提示
        self.lb2 = QLabel(self)
        self.lb2.setText("默认页长：256B")
        self.lb2.move(shape[0] * 0.5 + 20, 440)
        self.lb2.resize(150, 30)
        # 越界中断提示
        self.lb3 = QLabel(self)
        self.lb3.setText("越界中断！请重新输入")
        self.lb3.move(shape[0] * 0.5 + 20, 540)
        self.lb3.resize(150, 30)
        self.lb3.setVisible(False)

    def changealg(self, i):
        self.info.change_alg(i + 2)

    # 菜单动作
    def importdata(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'csv(*.csv)')
        if fname:
            self.pagelist.impdata(fname[0])

    def exportdata(self):
        fname = QFileDialog.getSaveFileName(self, 'save file', '/home', 'csv(*.csv)')
        if fname:
            self.pagelist.save_status(fname[0])

    def query(self):
        shape = self.shape
        addr = int(self.qle1.text())
        if not self.pagelist.get_one_page(addr):
            self.lb3.setVisible(True)
        else:
            self.lb3.setVisible(False)
            page = addr >> self.pagelist.ps
            self.pagelist.query(page, self.info)
            self.lb1.setText("缺页率{}/{}   {}".format(self.info.num_lack, self.info.num_query,
                                                    round(self.info.num_lack / self.info.num_query * 100, 1)))
            self.view.setModel(QtTable(self.pagelist.list))
            self.view.selectRow(page)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet_pyqt5())
    w = mywin((1080, 720))
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
