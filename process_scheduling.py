from PCB import PCBs
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
    def __init__(self,shape):
        super().__init__()
        self.pcb=PCBs()
        self.alg=1
        self.initUI(shape)
    def initUI(self,shape):
        self.setGeometry(300, 300, *shape)
        self.view=QTableView(self)
        self.view.setGeometry(0,0,shape[0]*0.5,shape[1]-33)
        self.view.setModel(QtTable(self.pcb.pcb))
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
        algselector.addItems(['短作业有限','先入先出','高响应比','优先级有限'])
        algselector.currentIndexChanged[int].connect(self.changealg)
        


    def changealg(self,i):
        self.alg=i


    def add(self):
        id=
        nt=
        at=
        rr=
        pr=
        self.pcb.add(id,nt,at,rr,pr)
    def timepass(self): 
        self.pcb.time+=1
        self.pcb.pcb.loc[0,'rest_time']-=1
        if self.pcb.pcb.loc[0,'rest_time']==0:
            self.pcb.pcb.dele()
        self.pcb.updata()
    # 菜单动作
    def importdata(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home','csv(*.csv)')
        if fname:
            self.pcb.impdata(fname[0])
    def exportdata(self):
        fname=QFileDialog.getSaveFileName(self,'save file','/home','csv(*.csv)')
        if fname:
            self.pcb.save_status(fname[0])


def main():
    app=QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet_pyqt5())
    w=mywin((1080,720))
    w.show()
    sys.exit(app.exec_())   
    
if __name__=="__main__":
    main()