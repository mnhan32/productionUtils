# -*- coding: utf-8 -*-
from shotgun_api3 import Shotgun
import sys,os,glob,platform,time


def writeLog(inStr):
	print inStr

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


if __name__=='__main__':
    SERVER_PATH = "https://wefxstudio.shotgunstudio.com"
    USER_NAME='mnhan'
    USER_KEY='*1a2b3c4d5F'
    
    sg=shotgun_handler(SERVER_PATH,USER_NAME,USER_KEY)
    allProjs=sg.getProjets([],['name'],True)
    userData=sg.getUser(USER_NAME,['projects','name'])
    print [x['name'] for x in userData[0]['projects']]
    #print [h for h in allProjs]

