try:
    import maya.standalone 
    maya.standalone.initialize(name='python') 
except: 
    pass
    
import maya.cmds as cmds
import os,sys, time
import json

#def generateDefault(sourceFile, tarJson, tarGeo, selSet):
def generateDefault(jsonObj, tarJson):
    
    selShape = cmds.listRelatives(jsonObj['animSet'], f=True)
    
    sel=[]
    for i in selShape:
        node = cmds.listRelatives(i, p=True, type='transform', f=True)[0]
        if not node in sel:
            sel.append(node) 
    
    data = []
    ctrls = {}
    ctrls['name'] = jsonObj['alias']
    ctrls['sourcefile'] = os.path.join( jsonObj['animPath'], jsonObj['animRig'])
    ctrls['timestamp'] = time.ctime(os.path.getmtime(ctrls['sourcefile']))
    ctrls['animSet'] = jsonObj['animSet']
    for i in sel:
        availableAttrs = cmds.listAttr(i, v=True, k=True, u=True)
        
        if availableAttrs:
            # check if attr is connected, if yes, ignore it
            attrs=[]
            for a in availableAttrs:
                if not cmds.listConnections('%s.%s'%(i, a), s=True, d=False):
                    attrs.append(a)
            ctrl={}
            if attrs:
                ctrl['attr'] = {} 
                ctrl['name'] = i            
                for k in attrs:
                    val = cmds.getAttr('%s.%s'%(i, k))
                    ctrl['attr'][k] = val
                data.append(ctrl)
    if data:   
        ctrls['ctrl'] = data    
        
    with open(tarJson, 'w') as f:
        json.dump(ctrls,f)
    f.close()

def getJsonObj(dirname,configFile):   
    f = open(os.path.join(dirname, configFile))
    config = json.load(f)
    f.close()
    return config

def main(config, configPath):
    #file open
    try:        
        filepath = os.path.join(config['animPath'], config['animRig'])
        result = cmds.file(filepath, o=True, f=True )

        basename = '.'.join(config['animRig'].split('.')[0:-1]) + '.json'
        tarJson = os.path.join(configPath, basename)
        generateDefault(config, tarJson)
        cmds.quit(force=True)
        print 'Finished generate default json for %s'%config['alias']
        
    except:
        print 'Failed generate json file for %s'%config['alias']
        
    exit()

if __name__ == '__main__':
    configFile = 'CFX_RigDefault.cfg'
    filePath = os.path.dirname(os.path.abspath(sys.argv[0]))
    configPath = os.path.join(filePath, "config")
    jsonObj = getJsonObj(configPath, configFile)

    passData = {}
    if sys.argv[1] in jsonObj.keys():
        passData = jsonObj[sys.argv[1]]
    
    if passData:
        main(passData, configPath)
    else:
        print 'Can not find related config for %s.'%sys.argv[1]
