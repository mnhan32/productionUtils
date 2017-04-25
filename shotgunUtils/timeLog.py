import os,sys,datetime,json,getpass,glob,ast
from shotgun_api3 import Shotgun

def clearTerminal():
    if not sys.platform == 'win32':
        os.system('clear')
    else:
        os.system('cls')

def getTimeStamp():
    timeStamp = datetime.datetime.now()
    cDate = timeStamp.strftime('%Y-%m-%d')
    cTime = timeStamp.strftime('%Y-%m-%d %H:%M:%S')
    strStamp = [cDate, cTime]
    return strStamp

def getUser(sg,user):
    #find user data
    filterArg=[['login','in',user]]
    userData = sg.find('HumanUser',filters=filterArg,fields=['projects','name','image'])[0]

    return userData

def batchSubmit(sg,inF,user):
    batchData=[]
    count = 0
    data=[]

    with open(inF, 'r') as f:
        for line in f:
            data.append(json.loads(line))
            count = count + 1

    for idx,i in enumerate(data):
        typ = i['type']
        if idx < count-1:
            if not typ == 'PAUSE' and not 'submit' in i.keys(): 
                tObj1 = datetime.datetime.strptime(i['cDate'],'%Y-%m-%d %H:%M:%S')
                tObj2 = datetime.datetime.strptime(data[idx+1]['cDate'],'%Y-%m-%d %H:%M:%S')
                timeDiff = (tObj2 - tObj1)
                dObj = getTimeStamp()[0]
                dur = timeDiff.total_seconds()/60.0
                if dur < 1:
                    dur = 1
                if typ == 'Misc':
                    timeLog = {
                            "project":{"type":"Project","id":108}, 
                            "user":{"type":"HumanUser","id":int(user)},
                            "duration":dur,
                            "date":dObj,
                            "description":i['des']
                            }
                else:
                    timeLog = {
                            "project":{"type":"Project", "id":i['project']['id']},
                            "entity":{"type":"Task", "id":i['id']},
                            "user":{"type":"HumanUser","id":int(user)},
                            "duration":dur,
                            "date":dObj
                        }
                batchData.append(timeLog)
                #batchData.append({"request_type":"create","entity_type":"TimeLog","data":timeLog})
                #print timeLog

        if idx == count-1:
            
            if not typ == 'PAUSE' and not 'submit' in i.keys():
                tObj1 = datetime.datetime.strptime(i['cDate'],'%Y-%m-%d %H:%M:%S')
                tObj2 = datetime.datetime.now()
                timeDiff = (tObj2 - tObj1)
                dObj = getTimeStamp()[0]
                dur = timeDiff.total_seconds()/60.0
                if dur < 1:
                    dur = 1
                if typ == 'Misc':
                    timeLog = {
                            "project":{"type":"Project","id":108}, 
                            "user":{"type":"HumanUser","id":int(user)},
                            "duration":dur,
                            "date":dObj,
                            "description":i[des]
                            }
                else:
                    timeLog = {
                            "project":{"type":"Project", "id":int(i['project'][u'id'])},
                            "entity":{"type":"Task", "id":int(i['id'])},
                            "user":{"type":"HumanUser","id":user},
                            "duration":dur,
                            "date":dObj
                        }
                batchData.append(timeLog)
                #batchData.append({"request_type":"create","entity_type":"TimeLog","data":timeLog})
                #print timeLog

    #batch submit
    print 'batch data submit.'
    if batchData:
        try:
            #print sg.batch(batchData)
            for i in batchData:
                sg.create('TimeLog',i)
            #mark submit
            if data:
                for j in data:
                    if not 'submit' in j.keys():
                        j['submit'] = getTimeStamp()[1]
                with open(inF, 'w+') as f:
                    for i in data:
                        json.dump(i,f)
                        f.write('\n')
            pass
        except:
            print 'submit fail.'


def pauseTask(inF):
    pauseData = {
            "cDate":getTimeStamp()[1],
            "type":"PAUSE"
            }
    with open(inF, 'a') as f:
        json.dump(pauseData, f)
        f.write('\n')


def getTask(sg, userid):
    
    #find active tasks in active project with human user
    filterArg=[
        ['sg_status_list','in',['ip','rdy']],
        ['task_assignees','is',{'type':'HumanUser','id':userid}],
        ['project.Project.sg_status', 'is', 'Active']
    ]
    activeTasks = sg.find('Task',filters=filterArg,fields=['name','sg_description','sg_status_list','step','entity','project'],order=[{'field_name':'project', 'direction':'asc'}])
    #print activeTasks
    return activeTasks


def writeMiscData(inF, mData, des=None):
    if mData == '2':
        des = 'learning'
    if mData == '1':
        des = 'meeting'
    if mData == '3':
        if des.strip() =='':
            des = 'no input'
    if mData.isdigit():
        miscData = {
                "cDate":getTimeStamp()[1],
                "type":"Misc",
                "des":des
             }
        with open(inF, 'a') as f:
            json.dump(miscData,f)
            f.write('\n')
    

if __name__ == '__main__':
    clearTerminal()    
    sg = None
    token = None
    cfg_data = None
    taskData = None
    cStatus = None
    taskFileList = []
    submitData = []
    __home = os.path.expanduser("~")
    __folder = '.shotgun_handler'
    __preference = os.path.join(__home,__folder)
    
    if not os.path.isdir(__preference):
        os.mkdir(__preference)

    __cfg = None

    while 1:
        if sg:
            print '\nWelcome %s'%cfg_data['user']
            print 'Shotgun Connection established: %s'%cfg_data['server']
        else:
            print '\n Welcome, no connection established yet.'
        
        if taskData:
            print '-------------------'
            for idx,i in enumerate(taskData):
                print '%d) Proj : %s, %s : %s ,  %s, status : %s'%(idx+1,i['project']['name'],i['entity']['type'],i['entity']['name'],i['step']['name'],i['sg_status_list'])
        print '-------------------'
        print 'L) Login'
        print 'P) Pause'
        print 'M) Misc'
        print 'S) Submit'
        print 'Q) Quit'

        if str(cStatus).isdigit():
            print '***** Working on %d ****'%(cStatus+1)
        elif cStatus == 'P':
            print '***** Pausing ******'
        elif cStatus == 'M':
            print '***** Misc *****'

        iData = raw_input('[L,Q,P,S,1,2.....]')
        
        if iData.upper() == 'M':
            clearTerminal()
            des=''
            taskFile = os.path.join(__preference,'%s.task'%getTimeStamp()[0])
            while 1:
                print '1) Meeting'
                print '2) Learning'
                print '3) Custom'
                print 'Q) Escape'
                mData = raw_input('[1-3,Q]')
                if mData.upper() == 'Q' or mData == '1' or mData == '2':
                    cStatus = 'M'
                    break                
                if mData == '3':
                    cStatus = 'M'
                    des = raw_input('[Custom]')
                    break

            writeMiscData(taskFile, mData, des)    
            clearTerminal() 

        if iData.upper() == 'Q':
            clearTerminal()
            if sg:
                sg.close()
            break

        if iData.upper() == 'L':
            __cfg_list = glob.glob(os.path.join(__preference,'*.cfg'))
            if __cfg_list:
                for idx,i in enumerate(__cfg_list):
                    print '%d) %s'%(idx+1,os.path.basename(i))
                
                while 1:
                    cfg_pick = raw_input('[1-%d] : '%len(__cfg_list))
                    try:
                        idx = int(cfg_pick)-1
                        if idx >= 0 and idx < len(__cfg_list):
                            __cfg = __cfg_list[idx]
                            
                            with open(__cfg, 'r') as f:
                                cfg_data = json.load(f)
                            
                            break

                    except:
                        pass

            else:
                server = raw_input('Server : ')
                userId = raw_input('Login : ')
                userPass = getpass.getpass()
                cfg_data = {
                        "server":server,
                        "user":userId,
                        "passwd":userPass
                        }

            try:
                print '#staring login'
                sg = Shotgun(cfg_data['server'],login=cfg_data['user'],password=cfg_data['passwd'])
                token = sg.get_session_token()
                user = cfg_data['user']
                #print cfg_data['server'].split('//')[1]
                __cfg = os.path.join(__preference, '%s.cfg'%cfg_data['server'].split('//')[1])
               
                with open(__cfg,'w') as f:
                    json.dump(cfg_data, f)
                
                print '..........login sucess'

                userData = getUser(sg,cfg_data['user'])
                #print userData
                taskData = getTask(sg,userData['id'])
                #print taskData



            except:
                print '..........login fail.'
                pass

            clearTerminal()

        if iData.upper() == 'P':
            if taskData:
                taskFile = os.path.join(__preference,'%s.task'%getTimeStamp()[0])
                pauseTask(taskFile)
                cStatus = 'P'

            clearTerminal()


        #Submit
        if iData.upper() == 'S':

            taskFileList = glob.glob(os.path.join(__preference,'*.task'))
            if taskFileList:
                clearTerminal()
                print '****** SUBMIT ******'
                while 1:
                    for idx,i in enumerate(taskFileList):
                        print '%d) %s'%(idx+1, os.path.basename(i))

                    submitTask = raw_input('Submit[1-%d]'%len(taskFileList))
                    
                    if submitTask.isdigit():
                        submitD = int(submitTask) - 1
                        if submitD >=0 and submitD < len(taskFileList):
                            batchSubmit(sg, taskFileList[submitD], userData['id'])

                            if taskData:
                                pauseTask(taskFileList[submitD])
                                cStatus = 'P'

                        break
                    elif submitTask == 'Q':
                        break

                #print submitData
            #clearTerminal()

        if taskData and iData.isdigit():
            idx = int(iData)-1
            if idx >= 0 and idx < len(taskData):
                print idx,cStatus
                if not idx == cStatus:
                    taskData[idx]['cDate'] = getTimeStamp()[1]
                    taskFile = os.path.join(__preference,'%s.task'%getTimeStamp()[0])
                    with open(taskFile,'a') as f:
                        json.dump(taskData[idx], f)
                        f.write('\n')

                    cStatus = idx

            clearTerminal()

        
            

        
