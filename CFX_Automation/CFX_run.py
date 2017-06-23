try:
    import maya.standalone 
    maya.standalone.initialize(name='python') 
except: 
    pass
    
import maya.cmds as cmds
import os,sys, time
import json
from utils import CFX_shotgunInfo

def getJsonObj(dirname,configFile):
    try:
        f = open(os.path.join(dirname, configFile))
        config = json.load(f)
        f.close()
        return config
    except:
        print 'error while loading json data from %s'%f
        return 0

def main(inputFile, configPath):
    basefile = os.path.dirname(inputFile)
    data = CFX_shotgunInfo.shotgunInfo(basefile)
    if data['err']:
        print data['err']
        raise
        exit()
    try:    
        result = cmds.file( inputFile, o=True, f=True )
    except:
        print 'failed to open %s'%inputFile
        exit()

if __name__ == '__main__':
    inputFile = sys.argv[1]
    if os.path.isfile(inputFile):    
        configPath = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir(configPath):
            print 'config folder %s not existed.'%sconfigPath
            raise
        main(inputFile , configPath)
    else:       
        print 'file %s not exists.'%inputFile
        raise