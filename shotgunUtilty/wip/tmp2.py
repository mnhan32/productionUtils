# -*- coding: utf-8 -*-

from shotgun_api3 import Shotgun

from PySide.QtCore import *
from PySide.QtGui import *
import userInterface2 as wefxShotgunUI

import sys,os,glob,platform,time,urllib


class shotgun_handler(object):
    def __init__(self,*args):
        try:   
            self.sg = Shotgun(args[0],login=args[1],password=args[2])
            self.loginUser=args[1] 
            print 'connection successed.'    
        except:
            print 'connection failed.'
    
    def getUser(self,*args):
        if args[0]:
            filterArg=[['login','in',[args[0]]]]
        else:
            filterArg=[]
        userData=self.sg.find('HumanUser',filters=filterArg,fields=args[1])
        if userData:  
            return userData
        else:
            return None

    def getProjets(self,*args):
        if args[0]:
            filterArg=[['name','in',args[0]]]
        else:
            filterArg=[]       
        proj=self.sg.find('Project',filters=filterArg,fields=args[1])    
        if proj:
            return proj	    
        else:
            return None

    def __filterGen(self):
        pass

    def __fieldGen(self):
        pass


class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent,Qt.SplashScreen)
        self.ui=wefxShotgunUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.SERVER_PATH = "https://wefxstudio.shotgunstudio.com"
        self.USER_NAME='mnhan'
        self.USER_KEY='*1a2b3c4d5F'
        
        
        self.__login()

    def __login(self):
        print 'login'
        self.sg=shotgun_handler(self.SERVER_PATH,self.USER_NAME,self.USER_KEY)		
        self.usrData=self.sg.getUser(self.USER_NAME,['projects','name','image'])
        self.__updateUsrThumbnail()
        self.__updateProject()
        self.statusBar().setStyleSheet("QStatusBar{text-align:right;padding-left:20px;background:rgba(50,50,50);color:rgb(200,200,200);font-weight:bold;}")
        self.statusBar().showMessage('There is no way to hide this stupid status bar in pyside')
        self.statusBar().setSizeGripEnabled(False)

    def __updateProject(self):
        #self.ui.cB_project.addItems([x['name'] for x in self.usrData[0]['projects']])
        pass

    def __updateAsset(self):
        pass

    def __updateUsrThumbnail(self):
        url = self.usrData[0]['image']
        data = urllib.urlopen(url).read()
        pixmap = QPixmap(50,50)
        pixmap.loadFromData(data)
        icon = QIcon(pixmap)
        self.ui.pushButton_3.setIcon(icon)

if __name__=='__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    ret = app.exec_()
    sys.exit(ret)
