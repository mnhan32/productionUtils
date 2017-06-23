import os, datetime 
def logInfo(infotype, infoMsg):
    pwd = os.path.dirname(__file__)
    logfolder = os.path.join(pwd,'../log')
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d.%H_%M_%S")
    logfile = 'log.%s'%timestamp
    print '%s : %s'%(infotype, infoMsg)
