# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/han/pyDev/tmp/usrInterface.ui'
#
# Created: Sat Jun 25 00:52:00 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(420, 165)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(420, 165))
        MainWindow.setMaximumSize(QtCore.QSize(420, 189))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(175, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(147, 147, 147))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(126, 124, 122))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(202, 202, 202))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(147, 147, 147))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(126, 124, 122))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(202, 202, 202))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(147, 147, 147))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(126, 124, 122))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(202, 202, 202))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.palette=palette
        MainWindow.setPalette(palette)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(420, 165))
        self.centralwidget.setMaximumSize(QtCore.QSize(420, 165))
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 424, 140))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(5, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.codeImg = QtGui.QPushButton(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.codeImg.sizePolicy().hasHeightForWidth())
        self.codeImg.setSizePolicy(sizePolicy)
        self.codeImg.setMinimumSize(QtCore.QSize(100, 75))
        self.codeImg.setMaximumSize(QtCore.QSize(100, 75))
        self.codeImg.setFocusPolicy(QtCore.Qt.NoFocus)
        self.codeImg.setText("")
        self.codeImg.setIconSize(QtCore.QSize(100, 75))
        self.codeImg.setFlat(True)
        self.codeImg.setObjectName("codeImg")
        self.horizontalLayout_2.addWidget(self.codeImg)
        spacerItem1 = QtGui.QSpacerItem(5, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.listView = QtGui.QListView(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setMinimumSize(QtCore.QSize(180, 80))
        self.listView.setMaximumSize(QtCore.QSize(180, 80))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.listView.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        font.setWeight(75)
        font.setBold(True)
        self.listView.setFont(font)
        self.listView.setFrameShape(QtGui.QFrame.NoFrame)
        self.listView.setFrameShadow(QtGui.QFrame.Plain)
        self.listView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listView.setAutoScroll(False)
        self.listView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listView.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.listView.setGridSize(QtCore.QSize(150, 20))
        self.listView.setObjectName("listView")
        self.verticalLayout_4.addWidget(self.listView)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.timer = QtGui.QLCDNumber(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timer.sizePolicy().hasHeightForWidth())
        self.timer.setSizePolicy(sizePolicy)
        self.timer.setMinimumSize(QtCore.QSize(140, 50))
        self.timer.setMaximumSize(QtCore.QSize(140, 50))
        self.timer.setFrameShape(QtGui.QFrame.NoFrame)
        self.timer.setDigitCount(8)
        self.timer.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.timer.setObjectName("timer")
        self.horizontalLayout_3.addWidget(self.timer)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.pB_timer = QtGui.QPushButton(self.layoutWidget)
        self.pB_timer.setMinimumSize(QtCore.QSize(0, 40))
        self.pB_timer.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pB_timer.setCheckable(True)
        self.pB_timer.setFlat(False)
        self.pB_timer.setObjectName("pB_timer")
        self.horizontalLayout_3.addWidget(self.pB_timer)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        spacerItem3 = QtGui.QSpacerItem(20, 130, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setContentsMargins(-1, -1, 10, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem4 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.usrImg = QtGui.QPushButton(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usrImg.sizePolicy().hasHeightForWidth())
        self.usrImg.setSizePolicy(sizePolicy)
        self.usrImg.setMinimumSize(QtCore.QSize(64, 64))
        self.usrImg.setMaximumSize(QtCore.QSize(64, 64))
        self.usrImg.setFocusPolicy(QtCore.Qt.NoFocus)
        self.usrImg.setText("")
        self.usrImg.setIconSize(QtCore.QSize(64, 64))
        self.usrImg.setFlat(False)
        self.usrImg.setObjectName("usrImg")
        self.horizontalLayout_4.addWidget(self.usrImg)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem5 = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.dayLog = QtGui.QListView(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dayLog.sizePolicy().hasHeightForWidth())
        self.dayLog.setSizePolicy(sizePolicy)
        self.dayLog.setMinimumSize(QtCore.QSize(80, 30))
        self.dayLog.setMaximumSize(QtCore.QSize(80, 30))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.dayLog.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.dayLog.setFont(font)
        self.dayLog.setFrameShape(QtGui.QFrame.NoFrame)
        self.dayLog.setFrameShadow(QtGui.QFrame.Plain)
        self.dayLog.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.dayLog.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.dayLog.setAutoScroll(False)
        self.dayLog.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.dayLog.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.dayLog.setGridSize(QtCore.QSize(90, 30))
        self.dayLog.setObjectName("dayLog")
        self.horizontalLayout_5.addWidget(self.dayLog)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setContentsMargins(-1, 2, 10, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 10))
        self.label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label.setObjectName("label")
        self.verticalLayout_6.addWidget(self.label)
        self.lb_loginSince = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_loginSince.sizePolicy().hasHeightForWidth())
        self.lb_loginSince.setSizePolicy(sizePolicy)
        self.lb_loginSince.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        font.setPointSize(8)
        self.lb_loginSince.setFont(font)
        self.lb_loginSince.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.lb_loginSince.setObjectName("lb_loginSince")
        self.verticalLayout_6.addWidget(self.lb_loginSince)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.verticalLayout_3.addLayout(self.verticalLayout_5)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pB_timer.setText(QtGui.QApplication.translate("MainWindow", "Timer/Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "last login since", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_loginSince.setText(QtGui.QApplication.translate("MainWindow", "2016-06-30 13:15", None, QtGui.QApplication.UnicodeUTF8))

