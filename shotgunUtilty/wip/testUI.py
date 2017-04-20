from PySide.QtCore import *
from PySide.QtGui import *

import sys
from shotgun_api3 import Shotgun
import time, pprint,datetime,urllib

SERVER_PATH = "https://wefxstudio.shotgunstudio.com"

USER_NAME= 'mnhan'
USER_KEY= '*1a2b3c4d5F'

if __name__=='__main__':
    app = QApplication(sys.argv)
    sg = Shotgun(SERVER_PATH, login=USER_NAME,password=USER_KEY)
    userData=sg.find('HumanUser',filters=[['login','in','mnhan']],fields=['due_date','projects','name','image'])
    #print userData[0]['id']
    #tarProjId=118
    #tasks = sg.find("Task",filters=[['project','is',{'type':'Project','id':118}],['task_assignees', 'is', {"type":"HumanUser", "id": 95}]], fields=['sg_status_list','id','entity','project','due_date',"step","tag_list",'content'])
    sT = time.time()
    print 'start'
    tasks = sg.find("Task",filters=[['task_assignees', 'is', {"type":"HumanUser", "id": 95}]], fields=['sg_status_list','id','entity','project','due_date',"step","tag_list",'content'])
    k=[h['entity']['id'] for h in [y for y in tasks if y['entity']!=None] if h['entity']['type']=='Shot']
    g=[h['entity']['id'] for h in [y for y in tasks if y['entity']!=None] if h['entity']['type']=='Asset']
    if k:
        seq=sg.find('Shot',filters=[['id','in',k]],fields=['sg_sequence','image'])
    if g:
        asset=sg.find('Asset',filters=[['id','in',g]],fields=['image'])
        #pprint.pprint(sg.find('Asset',filters=[['id','in',g]],fields=['image']))
    for i in tasks:
        if i['entity'] != None:
            if i['entity']['type']=='Shot':
                if k:
                    itemImage= [h['image'] for h in seq if i['entity']['id']==h['id']][0]
                    itemSeq= [h['sg_sequence'] for h in seq if i['entity']['id']==h['id']][0]
            elif  i['entity']['type']=='Asset':
                if g:
                    itemImage= [h['image'] for h in asset if i['entity']['id']==h['id']][0]
                    itemSeq= None
                
            i['sg_sequence']=itemSeq
            i['image']=itemImage

        else:
            i['sg_sequence']=None
            i['image']=None
    

    app.setStyle('cleanlooks')
    
    
    k=len(tasks)
    dataModel=QStandardItemModel(k,2)
    for d,i in enumerate(tasks):  
    
        if i['project']!=None:
            prjName = i['project']['name']
        else:
            prjName = 'no name'
        
        if i['entity']!=None:
            shotCode=i['entity']['name']
        else:
            shotCode='not assigned'
        #print i    
        
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
            
        '''
        pixmap = QPixmap(100,75)
        imgF = 'C:\Users\mnhan\Desktop\95.jpg'
        if i['image']!=None:
            imgF = i['image']
            data = urllib.urlopen(i['image']).read()
            pixmap.loadFromData(data)
        else:        
            pixmap.load(imgF)
            
        icon = QIcon(pixmap)
        '''
        
        item1 = QStandardItem('%s\n%s\n%s\n%s\n'%(prjName,typeName,shotCode,taskName))
        #item1.setIcon(icon)
        item2 = QStandardItem('\n\n%s\n%s\n'%('Due in : Days', '7/15 Hrs'))
        dataModel.setItem(d,0,item1)
        dataModel.setItem(d,1,item2)
    
    
    tableView= QTableView()
    tableView.show()
    tableView.setIconSize(QSize(100,75))
    tableView.verticalHeader().hide()
    tableView.horizontalHeader().hide()
    tableView.setSelectionBehavior(QAbstractItemView.SelectRows)

    
    tableView.setModel(dataModel)
    tableView.resizeRowsToContents()
    tableView.setColumnWidth(0,150)
    for i in range(k):
        if i>0:
            tableView.setRowHidden(i, True)
      
    totalTime = time.time()-sT
    print totalTime
    ret = app.exec_()
    sys.exit(ret)





    #tableView.setColumnWidth(1,120)
   
