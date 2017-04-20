# -*- coding: utf-8 -*-

from shotgun_api3 import Shotgun
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

    def getTask(self,*args):
        if args[0]:
            filterArg=[ ['task_assignees', 'is', {"type":"HumanUser", "id": args[0]}]]
        else:
            filterArg=[]
        
        #sample args[1] 
        #['sg_status_list','id','entity','project','start_date','due_date',"step","tag_list",'content']
        taskData=self.sg.find('Task',filters=filterArg,fields=args[1])
        #print filterArg
        #print args[1]
        
        #retreive seq data if task entity type is Shot
        k=[h['entity']['id'] for h in [y for y in taskData if y['entity']!=None] if h['entity']['type']=='Shot']
        g=[h['entity']['id'] for h in [y for y in taskData if y['entity']!=None] if h['entity']['type']=='Asset']
        
        if k:
            seq=self.sg.find('Shot',filters=[['id','in',k]],fields=['sg_sequence','image'])
        if g:
            asset=self.sg.find('Asset',filters=[['id','in',g]],fields=['image'])
            
        for i in taskData:
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
        
        if taskData:
            return taskData
        else:
            return None
    
    
    def getTimeLog(self,*args):
        pass
    
    def __filterGen(self):
        pass

    def __fieldGen(self):
        pass
