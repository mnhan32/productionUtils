from shotgun_handler import shotgun_handler
import getpass
from shotgun_api3 import Shotgun
import json
from PySide.QtCore import *
from PySide.QtGui import *
import sys,os,glob,platform,datetime,urllib,pprint

class taskWidget(QWidget):

    def __init__(self,parent=None):
        super(taskWidget,self).__init__(parent)#,Qt.FramelessWindowHint
        self.tableView= QTableView()
        self.tableView.setIconSize(QSize(100,75))
        self.tableView.verticalHeader().hide()
        #self.tableView.setHorizontalHeaderLabels(['Proj','Task','Des'])
        #self.tableView.horizontalHeader()
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.tableView)
        self.setLayout(layout)        
        
    def initUI(self,inDataModel):
        self.tableView.setModel(inDataModel)
        self.tableView.resizeRowsToContents()
        self.tableView.setColumnWidth(0,150)
        self.itemSel = QItemSelectionModel(inDataModel)
        self.tableView.clicked.connect(self.taskSelected)
        
    
    def taskSelected(self):
        #self.hide()
        print 'here'
        selR = self.tableView.selectedIndexes()
        for i in selR:
            k=self.tableView.model().data(i,role=Qt.EditRole)
            k=self.tableView.model().data(i,role=Qt.DisplayRole)
        '''
        a={'a':1,'t':{'c':'dadwa','k':'e21'},'date':str(datetime.date.today()),'time':str(datetime.datetime.now().time())}
        with open('C:\Users\mnhan\.wefxShotgun\data.json','a') as f:
            json.dump(a, f)
            f.write('\n')'''
        
        #targetWid.updateTaskTrigger()


if __name__=='__main__':
    
    

    serverName = raw_input("Server Path : ")
    userName = raw_input("User Name : ")
    passWd = getpass.getpass()
    sg = Shotgun(serverName,login=userName,password=passWd)
    
    #find user data
    filterArg=[['login','in',userName]]
    userData = sg.find('HumanUser',filters=filterArg,fields=['projects','name','image'])[0]

    #find active tasks in active project with human user
    filterArg=[
        ['sg_status_list','in',['ip','rdy']],
        ['task_assignees','is',{'type':'HumanUser','id':userData['id']}],
        ['project.Project.sg_status', 'is', 'Active']
    ]
    activeTasks = sg.find('Task',filters=filterArg,fields=['name','sg_description','sg_status_list','step','entity','project'],order=[{'field_name':'project', 'direction':'asc'}])
    
    #set header label
    taskData = QStandardItemModel(len(activeTasks),3)
    taskData.setHeaderData(0,Qt.Orientation.Horizontal,'project')
    taskData.setHeaderData(1,Qt.Orientation.Horizontal,'task')
    taskData.setHeaderData(2,Qt.Orientation.Horizontal,'des')
    
    for d,i in enumerate(activeTasks):
        item1 = QStandardItem('%s:%s %s:%s'%(i['project']['id'],i['project']['name'],i['entity']['type'],i['entity']['name']))
        item2 = QStandardItem('%s, %s, %s'%(i['id'],i['step']['name'],i['sg_status_list']))
        item3 = QStandardItem(i['sg_description'])
        idx = taskData.createIndex(d,0)
        taskData.setData(idx,QStandardItem('rwdwa21d'),Qt.EditRole)
        taskData.setData(idx,item1,Qt.DisplayRole)
        #taskData.setItem(d,0,item1)
        taskData.setItem(d,1,item2)
        taskData.setItem(d,2,item3)
    
        
    app = QApplication(sys.argv)
    app.setStyleSheet('')
    mainWin = taskWidget()    
    mainWin.initUI(taskData)
    mainWin.show()
    ret = app.exec_()
    sys.exit(ret)







'''
#find active project with human user
filterArg = [
    ['sg_status','is','Active'],
    ['users','is',{'type':'HumanUser','id':userData['id']}]
]
activeProj= sg.find('Project',filters=filterArg,fields=['project'])


filterArg=[
    ['user','is',{'type':'HumanUser','id':userData['id']}],
    ['project','in',activeProj],
    ['date','greater_than','2017-04-10'],
]

userTimeLog = sg.find('TimeLog',filters=filterArg,fields=['entity','project'])


for i in userTimeLog:
    filterArg=[
        ['id','is',i['entity']['id']]
    ]
    shotCode = sg.find_one('Task',filters=filterArg,fields= ['entity'])
    print shotCode
    print i
'''
'''
taskID= 11217
td = datetime.date.today()
timeLogData={
    'project':{'type':'Project', 'id':184},
    'entity':{'type': 'Task', 'id': 11217},
    'user':{'type':'HumanUser','id':userData['id']}
    'duration':60,
    'date':td
    }
}
sg.create('TimeLog',timeLogData)
'''
sg.close()
