from __future__ import print_function
from shotgun_api3 import Shotgun
import os,sys,getpass,json
import glob,platform,datetime,urllib,pprint
from  itertools import *

server = 
u = 
p = 
sg = Shotgun(server,login=u,password=p)


'''

filterArg = [
    ['Type':'TimeLog'],
    []
   
]
sg.find('TimeLog',filters=filterArg,fields=['entity'],order=[{'field_name':'user', 'direction':'asc'}])


'''
'''
filterArg = [
    ['task_assignees', 'is',{'type':'HumanUser','id':95}],
    ['project.Project.sg_status', 'is', 'Active'],
    ['step', 'is', {'type':'Step','id':12}]
]

meetingData= sg.find('Task',filters=filterArg, fields=['project','sg_status_list','entity','task_assignees'],oreder=[{'field_name':'user', 'direction':'asc'}])
'''

filterArg = [
    ['date','in_calendar_week',-1]
]

data= sg.find('TimeLog',filters=filterArg,fields=['user','entity','date','project','duration'],order=[{'field_name':'user', 'direction':'asc'},{'field_name':'date', 'direction':'asc'}])

filterArg = [
    ['sg_status_list','is','act']
]

userData = sg.find('HumanUser',filters=filterArg,fields=['name','entity'])
activeUser=[i['name'] for i in userData if not i['name'] == 'Shotgun Support']

#print data
logUser=[]
timelogAmt = 0

home_dir = os.path.expanduser('~')
f=open(os.path.join(home_dir,'timelog.txt'),'a')
print('__________________________________\n', file=f)
print('Time log from last week', file=f)
print('__________________________________\n', file=f)
for key, group in groupby(data,lambda x: x['user']['id']):
    #print key
    count = 0
    dur = 0
    
    for a in group:                
        if count == 0:
            logUser.append(a['user']['name'])
            print('USER : %s'%a['user']['name'], file=f)
            count += 1
        timelogAmt  +=1
        eName = None
        pName = None
        if 'entity' in a.keys():
            if a['entity']:
                eName = a['entity']['name']
        if 'project' in a.keys():
            pName = a['project']['name']
        dur += a['duration']
        
        print('Date : %s ,%s : %s, duration : %s hr.'%(a['date'], pName, eName, a['duration']), file=f)
    print('total hr in last week : %f hr'%dur, file=f)
    print('__________________________________\n', file=f)
print('total time log amount : %d'%timelogAmt, file=f)
print('__________________________________\n', file=f)

print('Missing time log from the following users:', file=f)
missingUser = [i for i in activeUser if i not in logUser]
for i in missingUser:
    print(i, file=f)


f.close()
sg.close()
#bookingData= sg.find('Booking',filters=filterArg, fields=['project','start_date','end_date','vacation','sg_status_list'])
#for i in bookingData:
#    print i
