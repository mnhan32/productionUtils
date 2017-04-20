# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *
import usrInterface as wefxShotgunUI
from shotgun_handler import shotgun_handler  
import sys,os,glob,platform,datetime,urllib,pprint

class taskWidget(QWidget):

    def __init__(self,parent=None):
        super(taskWidget,self).__init__(parent,Qt.FramelessWindowHint)
        self.tableView= QTableView()
        self.tableView.setIconSize(QSize(100,75))
        self.tableView.verticalHeader().hide()
        self.tableView.horizontalHeader().hide()
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.tableView)
        self.setLayout(layout)
        
        
    def initUI(self,inDataModel,baseWid):
        self.tableView.setModel(inDataModel)
        self.tableView.resizeRowsToContents()
        self.tableView.setColumnWidth(0,150)
        self.itemSel = QItemSelectionModel(inDataModel)
        self.tableView.clicked.connect(lambda : self.taskSelected(baseWid))
        
    
    def taskSelected(self,targetWid):
        self.hide()
        targetWid.updateTaskTrigger()


class Login(QDialog):

    def __init__(self, parent=None):
        super(Login, self).__init__(parent,Qt.FramelessWindowHint)
        self.nameLabel=QLabel('username',self)
        self.passwdLabel=QLabel('passwd',self)
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        self.buttonCancelLogin=  QPushButton('Cancel', self)
        self.buttonCancelLogin.clicked.connect(self.reject)
        
        layout = QVBoxLayout(self)
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        
        layout1.addWidget(self.nameLabel)
        layout1.addWidget(self.textName)
        layout2.addWidget(self.passwdLabel)
        layout2.addWidget(self.textPass)        
        layout3.addWidget(self.buttonLogin)
        layout3.addWidget(self.buttonCancelLogin)
        
        self.textPass.setEchoMode(QLineEdit.Password);
        


    def handleLogin(self):
        if (self.textName.text() != '' and
            self.textPass.text() != ''):
            self.accept()
        else:
            QMessageBox.warning(
                self, 'Error', "usrname and passwd can't be empty")

    def returnLoginData(self):
        return [self.textName.text(),self.textPass.text()]

class uiWidget(QMainWindow):
    def __init__(self,parent=None):
    
        super(uiWidget,self).__init__(parent)
        
        #init ui
        self.ui=wefxShotgunUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.__uiModify()
        
        #this should be replaced by login ui
        #and should use shadowed passwd someday
        self.SERVER_PATH = "https://wefxstudio.shotgunstudio.com"
        self.USER_NAME=''
        #self.USER_KEY='*1a2b3c4d5F'
        
        #pre-defined attr
        self.eventX=0
        self.eventY=0
        
        #
        self.timerVal='00:00:00' 
       
        #taskWidget window
        self.tW = None
        
        usrFolder= os.path.abspath(os.path.expanduser("~/"))
        self.prefFolder=os.path.join(usrFolder,'.wefxShotgun')
        if not os.path.isdir(self.prefFolder):
            os.mkdir(self.prefFolder,0774)

        #
        self.__login()
    
    def __uiModify(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.listView.setFocusPolicy(Qt.NoFocus)
        self.ui.dayLog.setFocusPolicy(Qt.NoFocus)
        
        
        self.statusBar().setSizeGripEnabled(False)
        #self.statusBar().addWidget(QLabel('label'),1)        
        #self.statusBar().insertWidget(1,QPushButton('ok'),0)
        self.statusBar().setStyleSheet("QStatusBar{padding-left:20px;background:rgba(50,50,50);color:rgb(200,200,200);font-weight:bold;}")
        self.statusBar().showMessage('drag me')
        #self.statusBar().show()
        
        self.ui.usrImg.clicked.connect(self.__login)
        self.ui.codeImg.clicked.connect(self.__taskList)
        self.__defaultTimer()
        
        pass    
    
    def updateTaskTrigger(self):
        dataRow=self.tW.tableView.selectedIndexes()[0].row()
        taskData=self.dataModel(dataRow)
        outData=taskData['project']['name']
        
    
    def __initTimer(self):
        self.timer=QElpasedTimer()
        self.timer.start()
        pass
        
    def __eventTimer(self):
        self.internalTimer = QTimer()
        self.internalTimer.timeout.connect(self.__updateDayLog)
        self.internalTimer.start(1000)
        pass
    
    def __defaultTimer(self):
        self.ui.timer.display('%s:%s:%s'%('00','00','00'))
        pass
    
    def __updateListView(self,inData=['Project Name','Seq/Asset','Code Name', 'Task Name']):
        tmpDataModel=QStringListModel(inData)
        self.ui.listView.setModel(tmpDataModel)
        pass
        
    def __updateDayLog(self):
        currentTime=datetime.datetime.now()-self.loginTime
        #print currentTime.seconds,str((currentTime.seconds//60)%60)
        #print str(currentTime.seconds//3600), str((currentTime.seconds//60)%60)
        self.dayLogDuration=QStringListModel(['%02dh%02dm'%(currentTime.seconds//3600, (currentTime.seconds//60)%60)])
        self.ui.dayLog.setModel(self.dayLogDuration)
        pass
        
    def __updateTimer(self,inTime):
        
        pass

    def __loginUpdateTrigger(self):
        self.usrData=self.sg.getUser(self.USER_NAME,['projects','name','image'])
        self.loginTime=datetime.datetime.today()
        self.__updateUsrThumbnail()
        self.__updateProject()
        self.__updateDayLog()
        self.__updateListView()
        self.__updateLoginSince(self.loginTime)
        self.__eventTimer()
        
        self.__usrTask=self.sg.getTask(self.usrData[0]['id'],['sg_status_list','id','entity','project','start_date','due_date',"step","tag_list",'content'])
        
    
    def __parseTaskData(self,inDataModelElement):
        if inDataModelElement['project']!=None:
                prjName = inDataModelElement['project']['name']
        else:
                prjName = 'no name'
            
        if i['entity']!=None:
            shotCode=inDataModelElement['entity']['name']
        else:
            shotCode='not assigned'

        
        if i['content']!=None:
            taskName=inDataModelElement['content']
        else:
            taskName=''
        
        if i['step']!=None:
            taskName+=' - '
            taskName+=inDataModelElement['step']['name']
        else:
            pass
        
        if inDataModelElement['sg_sequence']!=None:
            typeName=inDataModelElement['sg_sequence']['name']
        else:
            typeName='Asset'
        
        return [prjName,typeName,shotCode,taskName]
        
        
    def __taskList(self):
        print 'task'
        k=len(self.__usrTask)
        self.dataModel=QStandardItemModel(k,2)
        for d,i in enumerate(self.__usrTask):
            if i['project']!=None:
                prjName = i['project']['name']
            else:
                prjName = 'no name'
            
            if i['entity']!=None:
                shotCode=i['entity']['name']
            else:
                shotCode='not assigned'
    
            
            if i['content']!=None:
                taskName=i['content']
            else:
                taskName=''
            
            if i['step']!=None:
                taskName+=' - '
                taskName+=i['step']['name']
            else:
                pass
            
            if i['sg_sequence']!=None:
                typeName=i['sg_sequence']['name']
            else:
                typeName='Asset'
            
            #print i['image']
            
            pixmap = QPixmap(100,75)
            imgF = ''
            
            if i['image']!=None:
                imgF = i['image']
                
                data = urllib.urlopen(i['image']).read()
                pixmap.loadFromData(data)
            else:        
                pixmap.load(imgF)
            
            #pixmap.scaled(200,150).scaled(100,75)
            icon = QIcon(pixmap)
            
            
            item1 = QStandardItem('%s\n%s\n%s\n%s\n'%(prjName,typeName,shotCode,taskName))
            #item1.setIcon(icon)
            item2 = QStandardItem('\n\n%s\n%s\n'%('Due in : Days', '7/15 Hrs'))
            self.dataModel.setItem(d,0,item1)
            self.dataModel.setItem(d,1,item2)
            
        if self.tW == None:
            self.tW=taskWidget()
            self.tW.initUI(self.dataModel,self)
            
        self.tW.show()
        
        #uiTaskList=QDiag
    
    
    def __login(self):
        print 'login'
        __loginDialog=Login()
        __loginDialog.setPalette(self.ui.palette)
        if __loginDialog.exec_() == QDialog.Accepted:
            __loginData=__loginDialog.returnLoginData()
            if __loginData[0]!=self.USER_NAME:                 
                try:
                    self.sg=shotgun_handler.shotgun_handler(self.SERVER_PATH,__loginData[0],__loginData[1])
                    self.USER_NAME=__loginData[0]
                    self. __loginUpdateTrigger()
                    
                except:
                    print 'log in failed'
                    pass
            else:
                print 'login already'
                pass
        pass


    def __updateLoginSince(self,inDateTime):
        self.ui.lb_loginSince.setText(inDateTime.strftime('%Y-%m-%d %H:%M:%S'))
        pass
        
    def __updateProject(self):
        #self.ui.cB_project.addItems([x['name'] for x in self.usrData[0]['projects']])
        pass

    def __updateAsset(self):
        pass

    #not done
    #just copy/paste from usr thumbnail
    def __updateCodeThumbnail(self):
        url = self.taskData[0]['image']
        data = urllib.urlopen(url).read()
        pixmap = QPixmap(50,50)
        pixmap.loadFromData(data)
        icon = QIcon(pixmap)
        self.ui.code.setIcon(icon)
        pass
        
    def __updateUsrThumbnail(self):
        url = self.usrData[0]['image']
        
        # if image is cached, if not download it 
        usrThumbFolder=os.path.join(self.prefFolder,'usrThumb')
        self.usrThumb=os.path.join(usrThumbFolder,(self.USER_NAME+'.jpg'))
        
        if not os.path.isdir(usrThumbFolder):
            os.mkdir(usrThumbFolder)

        if not os.path.isfile(self.usrThumb):
            data = urllib.urlopen(url).read()
            img=QImage()
            img.loadFromData(data)
            #!!! need to figure out how to scale and save image in qt
            img.scaled(50,50)
            img.save(self.usrThumb)

        #
        pixmap = QPixmap(50,50)
        pixmap.load(self.usrThumb)
        icon = QIcon(pixmap)
        self.ui.usrImg.setIcon(icon)
        pass
                
    #move windows with frameless ui
    def mouseMoveEvent(self, event):
        super(uiWidget, self).mouseMoveEvent(event)
        if self.leftClick == True: 
            self.move(event.globalPos().x()-self.eventX,event.globalPos().y()-self.eventY)

    def mousePressEvent(self, event):
        super(uiWidget, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.leftClick = True
            self.eventX=event.pos().x()
            self.eventY=event.pos().y()

    def mouseReleaseEvent(self, event):
        super(uiWidget, self).mouseReleaseEvent(event)
        self.leftClick = False


if __name__=='__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('')
    mainWin = uiWidget()
    mainWin.show()
    ret = app.exec_()
    sys.exit(ret)