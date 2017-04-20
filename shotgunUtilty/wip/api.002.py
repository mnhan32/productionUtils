from shotgun_api3 import Shotgun
import time

SERVER_PATH = "https://wefxstudio.shotgunstudio.com"

USER_NAME='mnhan'
USER_KEY='*1a2b3c4d5F'

if __name__=='__main__':

    total_start_time = time.time()
    #sg = Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)
    sg = Shotgun(SERVER_PATH, login=USER_NAME,password=USER_KEY)
    connected_time = time.time() - total_start_time
    
    
    tarProj_start_time = time.time()
    
    #return only matching project id, extract id value from return dict
    tarProjName='TTD'
    tarProj=sg.find('Project',filters=[['name','is',tarProjName]])
    tarProjId= tarProj[0]['id']
    
    id_time = time.time() - tarProj_start_time
    print '%s id is %s'%(tarProjName,tarProjId)
    
    
    user_start_time = time.time()
    #get user id
    userName='MengHan Ho'
    userId=sg.find('HumanUser',filters=[['name','is',userName]])[0]['id']
    print '%s id is %s'%(userName,userId)
    user_time = time.time() - user_start_time
    
    
    timelog_start_time= time.time()
    #find specified filed data with filter. 
    #In this case, filter by tarProjId, userId    
    
    #find timelog of a user in a project
    k=sg.find('TimeLog',filters=[['project','is',{'type':'Project','id':tarProjId}],['user','is',{'type':'HumanUser','user':userName,'id':userId}]],fields=['user','duration','date','entity'])
    timelog_time = time.time() - timelog_start_time
    
    #SUM of timelog time of a user in a project
    summarize_start_time= time.time()
    totalTime=sg.summarize(entity_type='TimeLog',filters=[['project','is',{'type':'Project','id':tarProjId}],['user','is',{'type':'HumanUser','user':userName,'id':userId}]],summary_fields=[{'field':'duration','type':'sum'}])['summaries']['duration']
    summarize_time = time.time() - summarize_start_time
     
    #find shotCode by match taskId
    j=[x['entity']['id'] for x in k if x['entity']!=None]
    shotEntites=sg.find('Task',filters=[['id','in',j],['entity','is_not',None]],fields=['entity','name','id'])
    start_time= time.time()
  
    #----------------------
    #Print time log info
    
    print ''
    print '-------------------------------'
    print '### SHOTGUN PYTHON API TEST ###'
    print '-------------------------------'
    print ''
    print 'Project : %s'%tarProjName
    print 'User : %s'%userName
    print 'Total Time : %s hrs( %s mins)'%(totalTime/60.0,totalTime)
    print 'Total Log : %s'%len(k)
    
    for i,x in enumerate(k):
        if x['entity']!=None:
            taskName=x['entity']['name']
            taskId=x['entity']['id']
            
            matchShot=[d for d in shotEntites if d['id']==taskId]
            if matchShot:
                shotCode = matchShot[0]['entity']['name']
            else:
                shotCode='no assign'
        else:
            shotCode='no assign'
            taskName='no assign'
            
        print '#%02d Log date: %s, Shot code: %s , Task : %s , Time: %s hrs( %s mins)'%(i+1, x['date'],shotCode,taskName,x['duration']/60.0,x['duration'])

    
    print ''
    print '-------------------------------'
    print '### SHOTGUN PYTHON API TEST ###'
    print '-------------------------------'
    
    query_time=time.time()-start_time    
    elapsed_time = time.time() - total_start_time

    print ''
    print 'elapsed time for server connection : %s'%connected_time
    print 'elapsed time for proj query : %s'%id_time
    print 'elapsed time for user query : %s'%user_time
    print 'elapsed time for timelog query : %s'%timelog_time
    print 'elapsed time for summarize query : %s'%summarize_time
    print 'elapsed time for query job: %s'%query_time
    print 'Total elpased time : %s'%elapsed_time
    print ''

