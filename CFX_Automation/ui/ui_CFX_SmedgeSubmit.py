# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'T:\Han\productionUtils\CFX_Automation\ui\ui_CFX_SmedgeSubmit.ui'
#
# Created: Thu Jun 29 12:53:57 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(564, 637)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tV_file = QtGui.QTreeView(self.centralwidget)
        self.tV_file.setGeometry(QtCore.QRect(10, 40, 541, 451))
        self.tV_file.setFrameShadow(QtGui.QFrame.Sunken)
        self.tV_file.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tV_file.setProperty("showDropIndicator", False)
        self.tV_file.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tV_file.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tV_file.setObjectName("tV_file")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 500, 541, 91))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(90, 10, 461, 20))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 5, 81, 31))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 564, 17))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtGui.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSet_default_path = QtGui.QAction(MainWindow)
        self.actionSet_default_path.setObjectName("actionSet_default_path")
        self.actionOverwrite = QtGui.QAction(MainWindow)
        self.actionOverwrite.setCheckable(True)
        self.actionOverwrite.setObjectName("actionOverwrite")
        self.actionShow_Valiadtion = QtGui.QAction(MainWindow)
        self.actionShow_Valiadtion.setCheckable(True)
        self.actionShow_Valiadtion.setChecked(True)
        self.actionShow_Valiadtion.setObjectName("actionShow_Valiadtion")
        self.menuMenu.addAction(self.actionSet_default_path)
        self.menuMenu.addAction(self.actionOverwrite)
        self.menuMenu.addAction(self.actionShow_Valiadtion)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "CFX_SmedgeSubmit", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Process", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Current Root", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMenu.setTitle(QtGui.QApplication.translate("MainWindow", "Menu", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSet_default_path.setText(QtGui.QApplication.translate("MainWindow", "ChangeRoot", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOverwrite.setText(QtGui.QApplication.translate("MainWindow", "Overwrite?", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Valiadtion.setText(QtGui.QApplication.translate("MainWindow", "Show Valiadtion", None, QtGui.QApplication.UnicodeUTF8))

