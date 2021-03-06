# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_makeTx.ui'
#
# Created: Tue Apr  5 23:36:32 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(281, 501)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QRect(0, 0, 281, 461))
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pB_doMakeTx = QPushButton(self.frame)
        self.pB_doMakeTx.setGeometry(QRect(10, 360, 261, 61))
        self.pB_doMakeTx.setAcceptDrops(True)
        self.pB_doMakeTx.setFlat(False)
        self.pB_doMakeTx.setObjectName("pB_doMakeTx")
        self.lE_log = QLineEdit(self.frame)
        self.lE_log.setEnabled(True)
        self.lE_log.setGeometry(QRect(10, 430, 261, 21))
        self.lE_log.setAcceptDrops(False)
        self.lE_log.setAutoFillBackground(False)
        self.lE_log.setFrame(False)
        self.lE_log.setReadOnly(True)
        self.lE_log.setObjectName("lE_log")
        self.gB_overwrite = QGroupBox(self.frame)
        self.gB_overwrite.setGeometry(QRect(10, 150, 261, 51))
        self.gB_overwrite.setCheckable(True)
        self.gB_overwrite.setChecked(False)
        self.gB_overwrite.setObjectName("gB_overwrite")
        self.cB_overwrite = QCheckBox(self.gB_overwrite)
        self.cB_overwrite.setGeometry(QRect(11, 19, 91, 20))
        self.cB_overwrite.setObjectName("cB_overwrite")
        self.pB_deleteTx = QPushButton(self.gB_overwrite)
        self.pB_deleteTx.setGeometry(QRect(130, 14, 121, 31))
        self.pB_deleteTx.setObjectName("pB_deleteTx")
        self.tabWid = QTabWidget(self.frame)
        self.tabWid.setEnabled(True)
        self.tabWid.setGeometry(QRect(10, 10, 261, 141))
        self.tabWid.setMinimumSize(QSize(0, 0))
        self.tabWid.setTabShape(QTabWidget.Triangular)
        self.tabWid.setElideMode(Qt.ElideNone)
        self.tabWid.setDocumentMode(True)
        self.tabWid.setObjectName("tabWid")
        self.tabWid_folder = QWidget()
        self.tabWid_folder.setObjectName("tabWid_folder")
        self.gB_srouceFolder = QGroupBox(self.tabWid_folder)
        self.gB_srouceFolder.setGeometry(QRect(0, 10, 261, 101))
        self.gB_srouceFolder.setObjectName("gB_srouceFolder")
        self.cmB_sourceDirPath = QComboBox(self.gB_srouceFolder)
        self.cmB_sourceDirPath.setGeometry(QRect(10, 20, 201, 21))
        self.cmB_sourceDirPath.setAcceptDrops(True)
        self.cmB_sourceDirPath.setEditable(False)
        self.cmB_sourceDirPath.setInsertPolicy(QComboBox.InsertAtBottom)
        self.cmB_sourceDirPath.setDuplicatesEnabled(False)
        self.cmB_sourceDirPath.setObjectName("cmB_sourceDirPath")
        self.tB_sourceDirBrowse = QToolButton(self.gB_srouceFolder)
        self.tB_sourceDirBrowse.setGeometry(QRect(220, 20, 27, 21))
        self.tB_sourceDirBrowse.setObjectName("tB_sourceDirBrowse")
        self.cB_convertAll = QRadioButton(self.gB_srouceFolder)
        self.cB_convertAll.setGeometry(QRect(10, 80, 198, 17))
        self.cB_convertAll.setChecked(False)
        self.cB_convertAll.setObjectName("cB_convertAll")
        self.cB_subFolder = QRadioButton(self.gB_srouceFolder)
        self.cB_subFolder.setGeometry(QRect(10, 50, 121, 20))
        self.cB_subFolder.setChecked(True)
        self.cB_subFolder.setObjectName("cB_subFolder")
        self.sB_subLevel = QSpinBox(self.gB_srouceFolder)
        self.sB_subLevel.setGeometry(QRect(140, 50, 53, 22))
        self.sB_subLevel.setMinimum(0)
        self.sB_subLevel.setMaximum(1000)
        self.sB_subLevel.setProperty("value", 0)
        self.sB_subLevel.setObjectName("sB_subLevel")
        self.tabWid.addTab(self.tabWid_folder, "")
        self.tabWid_files = QWidget()
        self.tabWid_files.setObjectName("tabWid_files")
        self.gB_sourceFiles = QGroupBox(self.tabWid_files)
        self.gB_sourceFiles.setGeometry(QRect(0, 10, 261, 101))
        self.gB_sourceFiles.setObjectName("gB_sourceFiles")
        self.tB_sourceFileBrowse = QToolButton(self.gB_sourceFiles)
        self.tB_sourceFileBrowse.setGeometry(QRect(220, 70, 27, 21))
        self.tB_sourceFileBrowse.setObjectName("tB_sourceFileBrowse")
        self.tB_clearList = QToolButton(self.gB_sourceFiles)
        self.tB_clearList.setGeometry(QRect(220, 20, 27, 21))
        self.tB_clearList.setObjectName("tB_clearList")
        self.tB_removeSel = QToolButton(self.gB_sourceFiles)
        self.tB_removeSel.setGeometry(QRect(220, 40, 27, 21))
        self.tB_removeSel.setObjectName("tB_removeSel")
        self.lW_sourceFiles = QListWidget(self.gB_sourceFiles)
        self.lW_sourceFiles.setGeometry(QRect(10, 20, 201, 71))
        self.lW_sourceFiles.setSelectionMode(QAbstractItemView.MultiSelection)
        self.lW_sourceFiles.setObjectName("lW_sourceFiles")
        self.tabWid.addTab(self.tabWid_files, "")
        self.tabWid_maya = QWidget()
        self.tabWid_maya.setEnabled(True)
        self.tabWid_maya.setObjectName("tabWid_maya")
        self.gB_sourceShd = QGroupBox(self.tabWid_maya)
        self.gB_sourceShd.setGeometry(QRect(0, 10, 261, 101))
        self.gB_sourceShd.setMinimumSize(QSize(0, 0))
        self.gB_sourceShd.setFlat(False)
        self.gB_sourceShd.setObjectName("gB_sourceShd")
        self.rB_allShd = QRadioButton(self.gB_sourceShd)
        self.rB_allShd.setGeometry(QRect(11, 20, 46, 20))
        self.rB_allShd.setChecked(True)
        self.rB_allShd.setObjectName("rB_allShd")
        self.rB_selectedShd = QRadioButton(self.gB_sourceShd)
        self.rB_selectedShd.setGeometry(QRect(70, 20, 98, 20))
        self.rB_selectedShd.setObjectName("rB_selectedShd")
        self.cB_swapToTx = QCheckBox(self.gB_sourceShd)
        self.cB_swapToTx.setGeometry(QRect(10, 40, 181, 20))
        self.cB_swapToTx.setObjectName("cB_swapToTx")
        self.pB_toTx = QPushButton(self.gB_sourceShd)
        self.pB_toTx.setGeometry(QRect(150, 60, 101, 31))
        self.pB_toTx.setObjectName("pB_toTx")
        self.pB_toNonTx = QPushButton(self.gB_sourceShd)
        self.pB_toNonTx.setGeometry(QRect(50, 60, 91, 31))
        self.pB_toNonTx.setObjectName("pB_toNonTx")
        self.tabWid.addTab(self.tabWid_maya, "")
        self.tabWid_options = QTabWidget(self.frame)
        self.tabWid_options.setEnabled(True)
        self.tabWid_options.setGeometry(QRect(10, 210, 261, 141))
        self.tabWid_options.setTabPosition(QTabWidget.North)
        self.tabWid_options.setTabShape(QTabWidget.Triangular)
        self.tabWid_options.setElideMode(Qt.ElideNone)
        self.tabWid_options.setDocumentMode(True)
        self.tabWid_options.setObjectName("tabWid_options")
        self.tabWid_makeTx = QWidget()
        self.tabWid_makeTx.setObjectName("tabWid_makeTx")
        self.gB_makeTxBinary = QGroupBox(self.tabWid_makeTx)
        self.gB_makeTxBinary.setGeometry(QRect(0, 10, 261, 51))
        self.gB_makeTxBinary.setObjectName("gB_makeTxBinary")
        self.tB_sourceCmbBrowse = QToolButton(self.gB_makeTxBinary)
        self.tB_sourceCmbBrowse.setGeometry(QRect(220, 20, 27, 21))
        self.tB_sourceCmbBrowse.setObjectName("tB_sourceCmbBrowse")
        self.lE_cmdPath = QLineEdit(self.gB_makeTxBinary)
        self.lE_cmdPath.setGeometry(QRect(10, 20, 201, 21))
        self.lE_cmdPath.setReadOnly(True)
        self.lE_cmdPath.setObjectName("lE_cmdPath")
        self.gB_commandFlags = QGroupBox(self.tabWid_makeTx)
        self.gB_commandFlags.setGeometry(QRect(0, 70, 261, 51))
        self.gB_commandFlags.setCheckable(True)
        self.gB_commandFlags.setChecked(False)
        self.gB_commandFlags.setObjectName("gB_commandFlags")
        self.lE_cmdFlag = QLineEdit(self.gB_commandFlags)
        self.lE_cmdFlag.setGeometry(QRect(10, 20, 241, 21))
        self.lE_cmdFlag.setObjectName("lE_cmdFlag")
        self.tabWid_options.addTab(self.tabWid_makeTx, "")
        self.tabWid_option = QWidget()
        self.tabWid_option.setObjectName("tabWid_option")
        self.gB_saveTo = QGroupBox(self.tabWid_option)
        self.gB_saveTo.setGeometry(QRect(0, 10, 261, 51))
        self.gB_saveTo.setFlat(False)
        self.gB_saveTo.setCheckable(True)
        self.gB_saveTo.setChecked(False)
        self.gB_saveTo.setObjectName("gB_saveTo")
        self.cmB_tarDirPath = QComboBox(self.gB_saveTo)
        self.cmB_tarDirPath.setGeometry(QRect(10, 20, 201, 21))
        self.cmB_tarDirPath.setAcceptDrops(True)
        self.cmB_tarDirPath.setEditable(True)
        self.cmB_tarDirPath.setInsertPolicy(QComboBox.InsertAtBottom)
        self.cmB_tarDirPath.setDuplicatesEnabled(False)
        self.cmB_tarDirPath.setObjectName("cmB_tarDirPath")
        self.tB_tarDirBrowse = QToolButton(self.gB_saveTo)
        self.tB_tarDirBrowse.setGeometry(QRect(220, 20, 27, 21))
        self.tB_tarDirBrowse.setObjectName("tB_tarDirBrowse")
        self.gB_imageFilter = QGroupBox(self.tabWid_option)
        self.gB_imageFilter.setEnabled(True)
        self.gB_imageFilter.setGeometry(QRect(0, 70, 261, 51))
        self.gB_imageFilter.setCheckable(True)
        self.gB_imageFilter.setChecked(False)
        self.gB_imageFilter.setObjectName("gB_imageFilter")
        self.lE_imageFilter = QLineEdit(self.gB_imageFilter)
        self.lE_imageFilter.setGeometry(QRect(10, 20, 231, 21))
        self.lE_imageFilter.setObjectName("lE_imageFilter")
        self.tabWid_options.addTab(self.tabWid_option, "")
        self.tabWid_filter = QWidget()
        self.tabWid_filter.setObjectName("tabWid_filter")
        self.gB_extra = QGroupBox(self.tabWid_filter)
        self.gB_extra.setEnabled(True)
        self.gB_extra.setGeometry(QRect(0, 10, 261, 111))
        self.gB_extra.setCheckable(True)
        self.gB_extra.setChecked(False)
        self.gB_extra.setObjectName("gB_extra")
        self.pB_goOiio = QPushButton(self.gB_extra)
        self.pB_goOiio.setGeometry(QRect(170, 20, 79, 41))
        self.pB_goOiio.setObjectName("pB_goOiio")
        self.lE_oiioFlag = QLineEdit(self.gB_extra)
        self.lE_oiioFlag.setGeometry(QRect(20, 70, 231, 21))
        self.lE_oiioFlag.setText("")
        self.lE_oiioFlag.setObjectName("lE_oiioFlag")
        self.lE_suffix = QLineEdit(self.gB_extra)
        self.lE_suffix.setGeometry(QRect(60, 20, 101, 21))
        self.lE_suffix.setText("")
        self.lE_suffix.setObjectName("lE_suffix")
        self.label_suffix = QLabel(self.gB_extra)
        self.label_suffix.setGeometry(QRect(20, 20, 51, 16))
        self.label_suffix.setObjectName("label_suffix")
        self.label_oiioFlag = QLabel(self.gB_extra)
        self.label_oiioFlag.setGeometry(QRect(20, 50, 121, 16))
        self.label_oiioFlag.setObjectName("label_oiioFlag")
        self.tabWid_options.addTab(self.tabWid_filter, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 281, 20))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuCmd = QMenu(self.menubar)
        self.menuCmd.setObjectName("menuCmd")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.ac_confirm = QAction(MainWindow)
        self.ac_confirm.setCheckable(True)
        self.ac_confirm.setChecked(True)
        self.ac_confirm.setMenuRole(QAction.TextHeuristicRole)
        self.ac_confirm.setObjectName("ac_confirm")
        self.ac_currentList = QAction(MainWindow)
        self.ac_currentList.setEnabled(False)
        self.ac_currentList.setObjectName("ac_currentList")
        self.ac_quit = QAction(MainWindow)
        self.ac_quit.setObjectName("ac_quit")
        self.ac_createBatchFile = QAction(MainWindow)
        self.ac_createBatchFile.setCheckable(False)
        self.ac_createBatchFile.setObjectName("ac_createBatchFile")
        self.ac_aboutMakeTx = QAction(MainWindow)
        self.ac_aboutMakeTx.setObjectName("ac_aboutMakeTx")
        self.ac_aboutMe = QAction(MainWindow)
        self.ac_aboutMe.setEnabled(True)
        self.ac_aboutMe.setObjectName("ac_aboutMe")
        self.ac_aboutOIIO = QAction(MainWindow)
        self.ac_aboutOIIO.setObjectName("ac_aboutOIIO")
        self.menuMenu.addAction(self.ac_confirm)
        self.menuMenu.addAction(self.ac_currentList)
        self.menuMenu.addAction(self.ac_createBatchFile)
        self.menuMenu.addAction(self.ac_quit)
        self.menuCmd.addAction(self.ac_aboutMakeTx)
        self.menuCmd.addAction(self.ac_aboutOIIO)
        self.menuCmd.addSeparator()
        self.menuCmd.addAction(self.ac_aboutMe)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuCmd.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWid.setCurrentIndex(2)
        self.tabWid_options.setCurrentIndex(1)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QApplication.translate("MainWindow", "Make Tx", None))
        self.pB_doMakeTx.setText(QApplication.translate("MainWindow", "Go tx", None))
        self.gB_overwrite.setTitle(QApplication.translate("MainWindow", "Removal", None))
        self.cB_overwrite.setText(QApplication.translate("MainWindow", "Overwrite?", None))
        self.pB_deleteTx.setText(QApplication.translate("MainWindow", "Delete Tx", None))
        self.gB_srouceFolder.setTitle(QApplication.translate("MainWindow", "source folder", None))
        self.tB_sourceDirBrowse.setText(QApplication.translate("MainWindow", "...", None))
        self.cB_convertAll.setText(QApplication.translate("MainWindow", "Including All Sub Folders", None))
        self.cB_subFolder.setText(QApplication.translate("MainWindow", "Sub-Folder Level", None))
        self.tabWid.setTabText(self.tabWid.indexOf(self.tabWid_folder), QApplication.translate("MainWindow", "Folder", None))
        self.gB_sourceFiles.setTitle(QApplication.translate("MainWindow", "source files", None))
        self.tB_sourceFileBrowse.setText(QApplication.translate("MainWindow", "...", None))
        self.tB_clearList.setText(QApplication.translate("MainWindow", "c", None))
        self.tB_removeSel.setText(QApplication.translate("MainWindow", "-", None))
        self.tabWid.setTabText(self.tabWid.indexOf(self.tabWid_files), QApplication.translate("MainWindow", "Files", None))
        self.gB_sourceShd.setTitle(QApplication.translate("MainWindow", "source shader/texture", None))
        self.rB_allShd.setText(QApplication.translate("MainWindow", "ALL", None))
        self.rB_selectedShd.setText(QApplication.translate("MainWindow", "Selected", None))
        self.cB_swapToTx.setText(QApplication.translate("MainWindow", "Swap to tx after convert", None))
        self.pB_toTx.setText(QApplication.translate("MainWindow", " to tx", None))
        self.pB_toNonTx.setText(QApplication.translate("MainWindow", "to non tx", None))
        self.tabWid.setTabText(self.tabWid.indexOf(self.tabWid_maya), QApplication.translate("MainWindow", "Maya", None))
        self.gB_makeTxBinary.setTitle(QApplication.translate("MainWindow", "maketx binary", None))
        self.tB_sourceCmbBrowse.setText(QApplication.translate("MainWindow", "...", None))
        self.gB_commandFlags.setTitle(QApplication.translate("MainWindow", "Custom Command Flags", None))
        self.lE_cmdFlag.setText(QApplication.translate("MainWindow", "-u -oiio", None))
        self.tabWid_options.setTabText(self.tabWid_options.indexOf(self.tabWid_makeTx), QApplication.translate("MainWindow", "MakeTx", None))
        self.gB_saveTo.setTitle(QApplication.translate("MainWindow", "Different tx Destination", None))
        self.tB_tarDirBrowse.setText(QApplication.translate("MainWindow", "...", None))
        self.gB_imageFilter.setTitle(QApplication.translate("MainWindow", "Custom Filter for Browser", None))
        self.lE_imageFilter.setText(QApplication.translate("MainWindow", "jpg png bmp tif tga exr", None))
        self.tabWid_options.setTabText(self.tabWid_options.indexOf(self.tabWid_option), QApplication.translate("MainWindow", "Options", None))
        self.gB_extra.setTitle(QApplication.translate("MainWindow", "oiiotools", None))
        self.pB_goOiio.setText(QApplication.translate("MainWindow", "go oiio", None))
        self.label_suffix.setText(QApplication.translate("MainWindow", "suffix", None))
        self.label_oiioFlag.setText(QApplication.translate("MainWindow", "oiio command flags", None))
        self.tabWid_options.setTabText(self.tabWid_options.indexOf(self.tabWid_filter), QApplication.translate("MainWindow", "Extra", None))
        self.menuMenu.setTitle(QApplication.translate("MainWindow", "menu", None))
        self.menuCmd.setTitle(QApplication.translate("MainWindow", "help", None))
        self.ac_confirm.setText(QApplication.translate("MainWindow", " Confirmation", None))
        self.ac_currentList.setText(QApplication.translate("MainWindow", "Display List", None))
        self.ac_quit.setText(QApplication.translate("MainWindow", "Quit", None))
        self.ac_createBatchFile.setText(QApplication.translate("MainWindow", "Create Batch", None))
        self.ac_aboutMakeTx.setText(QApplication.translate("MainWindow", "About Maketx", None))
        self.ac_aboutMe.setText(QApplication.translate("MainWindow", "About", None))
        self.ac_aboutOIIO.setText(QApplication.translate("MainWindow", "About OIIO", None))

