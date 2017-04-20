# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *
import usrInterface as wefxShotgunUI
from shotgun_handler import shotgun_handler
   
import sys,os,glob,platform,datetime,urllib,pprint


class taskWidget(QWidget):
    def __init__(self,parent=None):
        super(taskWidget,self).__init__(parent)
        self.tableView= QTableView()
        self.tableView.setIconSize(QSize(100,75))
        self.tableView.verticalHeader().hide()
        self.tableView.horizontalHeader().hide()
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tableView)
        self.setLayout(layout)
        
    def initUI(self,inDataModel):
        self.tableView.setModel(inDataModel)
        self.tableView.resizeRowsToContents()
        self.tableView.setColumnWidth(0,150)

def go():
    global kk
    kk= taskWidget()
    kk.show()


    
if __name__=='__main__':
    app = QApplication(sys.argv)
    t=QWidget()
    layout = QVBoxLayout()
    b=QPushButton('go')
    b.clicked.connect(go)
    layout.addWidget(b)
    t.setLayout(layout)
    t.show()
    ret = app.exec_()
    sys.exit(ret)
