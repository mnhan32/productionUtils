from shotgun_api3 import Shotgun
import time, pprint,datetime

SERVER_PATH = "https://wefxstudio.shotgunstudio.com"

USER_NAME= 'mnhan'
USER_KEY= '*1a2b3c4d5F'

if __name__=='__main__':
    sg = Shotgun(SERVER_PATH, login=USER_NAME,password=USER_KEY)
    #userData=sg.find('HumanUser',filters=[['login','in','mnhan']],fields=['projects','name','image'])
    #print userData[0]['id']
    #tasks = sg.find("Task",filters=[['task_assignees', 'is', {"type":"HumanUser", "id": userData[0]['id']}],['entity','is',{'type':'Shot','id':2818}]], fields=['sg_status_list','id','entity','project'])
    #pprint.pprint(tasks)
    #pprint.pprint(sg.find('Project',filters=[],fields=['name']))

    #pprint.pprint(sg.schema_field_read('Shot'))
   
    tasks = sg.find("Task",filters=[['task_assignees', 'is', {"type":"HumanUser", "id": 95}]], fields=['sg_status_list','id','entity','project','due_date',"step","tag_list",'content'])
    k=[h['entity']['id'] for h in [y for y in tasks if y['entity']!=None] if h['entity']['type']=='Shot']
    g=[h['entity']['id'] for h in [y for y in tasks if y['entity']!=None] if h['entity']['type']=='Asset']
    if k:
        seq=sg.find('Shot',filters=[['id','in',k]],fields=['sg_sequence','image'])
    if g:
        asset=sg.find('Asset',filters=[['id','in',g]],fields=['image'])
        pprint.pprint(sg.find('Asset',filters=[['id','in',g]],fields=['image']))
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
            
    
    pprint.pprint(tasks)
    print len(tasks)


