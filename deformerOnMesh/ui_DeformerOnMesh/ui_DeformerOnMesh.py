# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/T/MayaScriptDev/deformerOnMesh/ui_DeformerOnMesh/ui_DeformerOnMesh.ui'
#
# Created: Sat Jun 10 23:48:10 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(211, 274)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.btn_run = QtGui.QPushButton(self.frame)
        self.btn_run.setGeometry(QtCore.QRect(0, 30, 191, 51))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_run.sizePolicy().hasHeightForWidth())
        self.btn_run.setSizePolicy(sizePolicy)
        self.btn_run.setObjectName("btn_run")
        self.cB_forceNew = QtGui.QCheckBox(self.frame)
        self.cB_forceNew.setGeometry(QtCore.QRect(0, 10, 131, 20))
        self.cB_forceNew.setObjectName("cB_forceNew")
        self.line_3 = QtGui.QFrame(self.frame)
        self.line_3.setGeometry(QtCore.QRect(0, 90, 191, 16))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gB_setting = QtGui.QGroupBox(self.frame)
        self.gB_setting.setGeometry(QtCore.QRect(0, 110, 191, 91))
        self.gB_setting.setCheckable(True)
        self.gB_setting.setChecked(False)
        self.gB_setting.setObjectName("gB_setting")
        self.dSB_falloff = QtGui.QDoubleSpinBox(self.gB_setting)
        self.dSB_falloff.setGeometry(QtCore.QRect(110, 60, 71, 23))
        self.dSB_falloff.setMaximum(100.0)
        self.dSB_falloff.setSingleStep(0.1)
        self.dSB_falloff.setProperty("value", 20.0)
        self.dSB_falloff.setObjectName("dSB_falloff")
        self.label_2 = QtGui.QLabel(self.gB_setting)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 91, 16))
        self.label_2.setObjectName("label_2")
        self.sB_growth = QtGui.QSpinBox(self.gB_setting)
        self.sB_growth.setGeometry(QtCore.QRect(110, 30, 71, 23))
        self.sB_growth.setProperty("value", 3)
        self.sB_growth.setObjectName("sB_growth")
        self.label = QtGui.QLabel(self.gB_setting)
        self.label.setGeometry(QtCore.QRect(10, 60, 91, 16))
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 211, 29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Defomer on Surface", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_run.setText(QtGui.QApplication.translate("MainWindow", "Generate", None, QtGui.QApplication.UnicodeUTF8))
        self.cB_forceNew.setText(QtGui.QApplication.translate("MainWindow", "Force New Build", None, QtGui.QApplication.UnicodeUTF8))
        self.gB_setting.setTitle(QtGui.QApplication.translate("MainWindow", "Setting", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Growth Step", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Falloff (%)", None, QtGui.QApplication.UnicodeUTF8))

