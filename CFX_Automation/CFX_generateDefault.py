try:
    import maya.standalone 
    maya.standalone.initialize(name='python') 
except: 
    pass
    
import maya.cmds as cmds
import os,sys, time
import json, glob
from utils import CFX_utils

#def generateDefault(sourceFile, tarJson, tarGeo, selSet):
def generateDefault(jsonObj, tarJson):

    #ctlNs = cmds.ls("*:%s"%jsonObj['ctrlSet'], type='objectSet')
    #ctl = cmds.ls(jsonObj['ctrlSet'], type='objectSet')#if no namespace
    #target = ctlNs + ctl

    selShape = cmds.listRelatives(jsonObj['ctrlSet'], f=True)

    sel=[]
    for i in selShape:
        node = cmds.listRelatives(i, p=True, type='transform', f=True)[0]
        if not node in sel:
            sel.append(node)

    ctrls = {} 
    ctrl = {}   
    ctrls['name'] = jsonObj["animRigName"]
    ctrls['sourcefile'] = cmds.file(q=True, sn=True)
    ctrls['timestamp'] = time.ctime(os.path.getmtime(ctrls['sourcefile']))
    ctrls['animSet'] = jsonObj['ctrlSet']
  
    for i in sel:
        availableAttrs = cmds.listAttr(i, v=True, k=True, u=True)
        
        if availableAttrs:
            # check if attr is connected, if yes, ignore it
            attrs=[]
            for a in availableAttrs:
                if not cmds.listConnections('%s.%s'%(i, a), s=True, d=False):
                    attrs.append(a)

            if attrs:
                if i not in ctrl.keys():
                    ctrl[i] = {}
                for k in attrs:
                    val = cmds.getAttr('%s.%s'%(i, k))
                    ctrl[i][k] = val
    if len(ctrl):
        ctrls['ctrl'] = ctrl
    with open(tarJson, 'w') as f:
        json.dump(ctrls,f)
    f.close()

def main(config, version=None):
    #file open
    try:
        if version:
            print version
            filePattern = config["animRigName"] +'.v'+  version.zfill(2) +'.'+ config["animRigType"]
            filePath = os.path.join(config['animRigPath'], filePattern)
            if not os.path.isfile(filePath):
                print 'Can not find associated version %s'%filePath
                raise
        else:
            print 'eles'
            filePattern = config['animRigName'] +'.v*.' + config['animRigType']
            print filePattern
            filePath = os.path.join(config['animRigPath'], filePattern)
            print filePath
            print glob.glob(filePath)
            fileList = glob.glob(filePath)
            fileList = sorted(fileList)
            print fileList 
            if fileList:
                filePath = fileList[-1]
            else:
                print 'Can not find associated files with pattern %s'%filePath
                raise
        result = cmds.file(filePath, o=True, f=True )
        basename = os.path.basename(result)
        jsonName = '.'.join(basename.split('.')[0:-1]) + '.json'
        tarJson = os.path.join(config["animRigPath"], jsonName)

        generateDefault(config, tarJson)
        cmds.quit(force=True)
        print 'Finished generate default json for %s'%config[ "animRigName"]
        
    except:
        print 'Failed generate json file for %s'%config[ "animRigName"]
        
    exit()

if __name__ == '__main__':
    jsonConfig = CFX_utils.getConfig('CFX')

    passData = {}
    if sys.argv[1] in jsonConfig.keys():
        passData = jsonConfig[sys.argv[1]]
    
    if passData:
        if len(sys.argv) > 2:
            version = sys.argv[2]
        else:
            version = None
        main(passData, version)
    else:
        print 'Can not find related config for %s.'%sys.argv[1]
