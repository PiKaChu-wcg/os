from PCB import PCBs
import pandas as pd
import numpy as np
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qdarkstyle import load_stylesheet_pyqt5
import time

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
    def __init__(self,shape):
        super().__init__()
        self.pcb=PCBs()
        self.initUI(shape)
    def initUI(self,shape):
        self.setGeometry(300, 300, *shape)
        self.view1=QTableView(self)
        self.view1.setGeometry(0,33,shape[0]*0.5,shape[1]*0.5-33)
        self.view1.setModel(QtTable(self.pcb.pcb[0]))
        self.view2=QTableView(self)
        self.view2.setGeometry(0,shape[1]*0.5,shape[0]*0.5,shape[1]*0.5)
        self.view2.setModel(QtTable(self.pcb.pcb[1]))
        #菜单项
        menubar = self.menuBar()
        dataMenu = menubar.addMenu('&Data')
        impAct = QAction('Import', self)    
        expAct = QAction('Export',self)
        impAct.triggered.connect(self.importdata)
        expAct.triggered.connect(self.exportdata)
        dataMenu.addAction(impAct)
        dataMenu.addAction(expAct)
        # 下拉框,选择算法
        algselector=QComboBox(self)
        algselector.setGeometry(shape[0]*0.5+20,50,150,20)
        algselector.addItems(['先入先出','短作业有限','高响应比','优先级有限'])
        algselector.currentIndexChanged[int].connect(self.changealg)
        
        self.qle1=QLineEdit(self)
        self.qle1.move(shape[0]*0.5+20,120)
        self.qle1.resize(150,30)
        self.qle1.setPlaceholderText("id")

        self.qle2=QLineEdit(self)
        self.qle2.move(shape[0]*0.5+20,220)
        self.qle2.resize(150,30)
        self.qle2.setPlaceholderText("等待时间")

        self.qle3=QLineEdit(self)
        self.qle3.move(shape[0]*0.5+20,320)
        self.qle3.resize(150,30)
        self.qle3.setPlaceholderText("运行时间")

        self.qle4=QLineEdit(self)
        self.qle4.move(shape[0]*0.5+20,420)
        self.qle4.resize(150,30)
        self.qle4.setPlaceholderText("优先级")

        self.btn1=QPushButton("新增",self)
        self.btn1.move(shape[0]*0.5+20,520)
        self.btn1.clicked.connect(self.add)

        self.btn2=QPushButton("开始",self)
        self.btn2.move(shape[0]*0.5+20,620)
        self.btn2.clicked.connect(self.turn)

        self.interval=1000

        self.timer=QTimer(self)
        self.timer.timeout.connect(self.timeout)

    def turn(self):
        s=self.sender()
        if s.text()=='开始':
            self.timer.start(self.interval)
            s.setText('暂停')
        else:
            self.timer.stop()
            s.setText('开始')

    def refresh(self):
        self.view1.setModel(QtTable(self.pcb.pcb[0]))
        self.view2.setModel(QtTable(self.pcb.pcb[1]))
    def changealg(self,i):
        self.pcb.alg=i+1


    def add(self):
        id=int(self.qle1.text())
        wt=int(self.qle2.text())
        rt=int(self.qle3.text())
        pr=int(self.qle4.text())                                                                                                                                                                                                                                    
        self.pcb.add(id,wt,rt,pr)
        self.refresh()
    def timepass(self): 
        self.pcb.timepass()
        self.refresh()
    # 菜单动作
    def importdata(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home','csv(*.csv)')
        if fname:
            self.pcb.impdata(fname[0])
        self.refresh()
    def exportdata(self):
        fname=QFileDialog.getSaveFileName(self,'save file','/home','csv(*.csv)')
        if fname:
            self.pcb.save_status(fname[0])

    def timeout(self):
        self.timepass()
        self.timer.start(self.interval)

    

def main():
    app=QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet_pyqt5())
    w=mywin((1080,720))
    w.show()


    sys.exit(app.exec_())   
    
if __name__=="__main__":
    main()