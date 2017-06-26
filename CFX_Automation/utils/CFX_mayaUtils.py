import maya.cmds as cmds
import os, glob, json

def returnWEFXTag(inputName):
    nspace = cmds.ls(inputName,l=True,sns=True)[1]
    baseName = inputName.split('|')[-1]
    if not nspace == ':':
        baseName = baseName.split(':')[-1]
    baseName = baseName.split('_')
    return baseName

def swapReference(rigConfig):
    sceneName = cmds.file(q=True, sceneName=True)
    refs = cmds.file(q=True, r=True)
    #print config
    if refs:
        for ref in refs:                    
            rfn = cmds.referenceQuery(ref, rfn=True)
            fpath = cmds.referenceQuery(rfn, filename=True, wcn=True)
            if cmds.referenceQuery(rfn, il=True):
                print '%s is loaded'%rfn
                return True
            else:
                baseRig = os.path.basename(fpath)
                rigName = baseRig.split('.')[0]    #need to fix if naming change
                #print rigName
                if rigName in rigConfig.keys():
                    print 'MATCH rigConfig %s'%rigName
                    targetRig = os.path.join(rigConfig[rigName]['animRigPath'], baseRig)
                    #print targetRig
                    if os.path.isfile(targetRig):
                        print 'REF FILE'
                        cmds.file(targetRig, lr=rfn)
                    return True
                else:
                    print 'rigConfig key: %s not existed.'%rigName
                    return False 
    else:
        print 'there is no reference existed in file %s'%sceneName
        return False

#Naming need to change if rig file naming change
def exportAnimationNode(outPath, rigConfig, tarSet):
    print 'entrering animation node exporting stage.'
    #export animation node, and json
    ctlNs = cmds.ls("*:WEFX_*_*", type='objectSet')
    ctl = cmds.ls("WEFX_*_*", type='objectSet')#if no namespace
    target = ctlNs + ctl

    availableSet = getSelectionSetMember(rigConfig, 'ctrlSet')
    #print availableSet
    if not availableSet:
        sceneName = cmds.file(q=True, sceneName=True)
        print 'no aviableSet in the file %s'%sceneName
        return False
    count = 0
    animData={}
    allNode = []
    for k in availableSet:
        tag = availableSet[k]['tag']
        sel = availableSet[k]['member']
        allNode += sel
        animationNodeType =availableSet[k]['anmNodeType']
        #print animationNodeType

        animData[count] = {}
        nspace = cmds.ls(k,l=True,sns=True)[1]
        if nspace==':':
            nspace = ''           
        animData[count]['namespace'] = nspace

        #print nspace
                
        animData[count]['targetAsset'] = tag
        filePattern = '%s_*.%s'%(rigConfig[tag]['animRigName'], rigConfig[tag]['animRigType'])#need to fix if naming change
        targetPath = os.path.join(rigConfig[tag]['animRigPath'],filePattern)
        fileList = glob.glob(targetPath)
        animData[count]['targetRigFile'] = sorted(fileList)[-1]

        version = cmds.getAttr('%s.WEFX_version'%k)    
        #print version
        if not version == 0:
            diffVersionFile =  rigConfig[tag[1]]['animRigName']+'V%s'%version.zfill(2)+ rigConfig[tag[1]]['animRigType']#need to fix if naming change
            if os.path.isfile(diffVersionFile):
                animData[count]['targetRigFile'] = diffVersionFile
        
        animData[count]['animCtl'] = {}
        animData[count]['nonKeyCtl'] = {}
        animNodes = []

        for node in sel:
            availableAttrs = cmds.listAttr(node, v=True, k=True, u=True)

            if availableAttrs:                
                for a in availableAttrs:
                    aNode = cmds.listConnections('%s.%s'%(node, a), s=True, d=False, scn=True)                    
                    if aNode:
                        #write connection
                        for n in aNode:                            
                            if cmds.objectType(n) in animationNodeType:   
                                if not node in animData[count]['animCtl'].keys():
                                    animData[count]['animCtl'][node] = {}      
                                animData[count]['animCtl'][node][a] = n
                                animNodes.append(n)                                                        
                    else:
                        #write data
                        currentVal = cmds.getAttr('%s.%s'%(node, a))
                        if not node in animData[count]['nonKeyCtl'].keys():
                            animData[count]['nonKeyCtl'][node] = {}
                        animData[count]['nonKeyCtl'][node][a] = currentVal
                  
    cmds.select(allNode, r=True)
    sceneName = cmds.file(q=True, sceneName=True)
    anmNodeFile = 'anmNode.' + '.'.join(sceneName.split('.')[-3:])
    extFile = os.path.join(outPath, anmNodeFile )
    tmp = 'anmNode.' + '.'.join(sceneName.split('.')[-3:-1]) + '.json'
    extJson = os.path.join(outPath,tmp)
    outFile = cmds.file(extFile, force=True, type='mayaAscii',eas=True)
    animData[count]['animFile'] = outFile

    count += 1

    with open( extJson, 'w') as f:
        json.dump(animData,f)
    return extJson
    print 'finish exporting animation data.'


def generateCleanAnimation(config):
    print 'generate clean animation file stage'
    for g in config:
        if not g == 'outFile':
            print config[g]['targetRigFile']
            if os.path.isfile(config[g]['targetRigFile']):
                ref =cmds.file(config[g]['targetRigFile'],r=True,ignoreVersion=True,mergeNamespacesOnClash=False,ns=config[g]['namespace'],options="v=0;")
            
            if 'animFile' in config[g].keys():
                cmds.file(config[g]['animFile'], i=True, namespace=":", options="mo=0")
                for i in config[g]['animCtl'].keys():
                    for attr in config[g]['animCtl'][i].keys():
                        cmds.connectAttr('%s.output'%config[g]['animCtl'][i][attr], '%s.%s'%(i,attr), f=True)

            for i in config[g]['nonKeyCtl'].keys():
                for attr in config[g]['nonKeyCtl'][i].keys():
                    cmds.setAttr('%s.%s'%(i,attr), config[g]['nonKeyCtl'][i][attr])


def extendAnimPrePostRoll(selection, config, sf, ef, preRollNum, postRollNum, defaultNum):
    print 'extend here'
    for sel in selection:
        # find available attrs
        if not cmds.objExists(sel):
            print '%s not exist'
        
        
       # print sel
        attrs = cmds.listAttr(sel, v=True, k=True, u=True)
        #print attrs
        #print '#####################'
        if attrs:
            for attr in attrs:
                attrValidate = False
                if not config == None:
                    tarData = removeNameSapce(sel)
                    if 'ctrl' in config.keys()   :          
                        if tarData in config['ctrl'].keys():
                            if attr in config['ctrl'][tarData].keys():
                                defaultVal = config['ctrl'][tarData][attr]
                                attrValidate = True
                                #print defaultVal
                else:
                    connection = cmds.listConnections('%s.%s'%(sel, attr), s=True, d=True)
                    if connection:
                        if cmds.objectType(connection[0]) in ["animCurveTA", "animCurveTL","animCurveTT","animCurveTU"]:
                            defaultVal = cmds.attributeQuery(attr, node=sel, ld=True)[0]
                            attrValidate = True
                    else:
                        defaultVal = cmds.attributeQuery(attr, node=sel, ld=True)[0]
                        attrValidate = True

                if attrValidate:
                    #print sel, attr, defaultVal
                    keys = cmds.keyframe(sel, at=attr, q=True)
                    #print attr, 'KEY', keys
                    #defaultVal = cmds.attributeQuery(attr, node=sel, ld=True)
                    #print defaultVal
                    
                    #print '######--------#######'
                    #print defaultVal, sel
                    if keys:
                        #print sel
                        #print 'KEYED' 
                        vals = cmds.keyframe(sel, at=attr,t=(keys[0], keys[-1]), q=True, vc=True)
                        keyRange = range(int(sf), int(ef)+1)
                        matchRange = sorted(list(set(keyRange) & set(keys)))
                        if matchRange:
                            if not matchRange[0] == sf:
                                cmds.setKeyframe(sel, at=attr, insert=True, t=(sf,sf))
                            if not matchRange[-1] == ef:
                                cmds.setKeyframe(sel, at=attr, insert=True, t=(ef,ef))
                            
                        else:
                            #problem
                            if keys[-1] < sf:
                                if not cmds.setInfinity(sel, at=attr, q=True, poi=True)[0] == 'constant':
                                    cmds.bakeResults(sel, at=attr, t=(sf, ef), sb=1)
                                else:
                                    cmds.setKeyframe(sel, at=attr, insert=True, t=(sf,sf))
                                    
                            if keys[0] > ef:       
                                if not cmds.setInfinity(sel, at=attr, q=True, pri=True)[0] == 'constant':
                                    cmds.bakeResults(sel, at=attr, t=(sf, ef), sb=1)
                                else:
                                    cmds.setKeyframe(sel, at=attr, insert=True, t=(ef,ef)) 
                        #remove frame outside sf to ef
                        if keys[0] < sf:
                            cmds.cutKey(sel, at=attr, t=(keys[0],sf-1), clear=True)
                        if keys[-1] > ef:
                            cmds.cutKey(sel, at=attr, t=(ef+1,keys[-1]), clear=True)
                        setPrePostRoll(1,1,preRollNum,postRollNum,sel,attr)
                        preRollToDefault(defaultNum, defaultVal, sel, attr)
                    else:
                        #print 'no KEY'
                        #print sel
                        sfVal = cmds.getAttr('%s.%s'%(sel,attr))
                        #print 'HERE2222', sfVal, defaultVal
                        if not sfVal == defaultVal:                    
                            cmds.setKeyframe(sel, at=attr, t=(sf,sf), v=sfVal)
                            #print sel  
                            setPrePostRoll(1,0,preRollNum,postRollNum,sel,attr)
                            #print 'done pre post'
                            preRollToDefault(defaultNum, defaultVal, sel, attr)
                            #print 'done to default'
                            #print attr
                        else:
                            pass
        #print '---------------------------------------'
    print 'finish extended'

def setPrePostRoll(preRoll, postRoll, preRollNum, postRollNum, obj, attr):    
    keys = cmds.keyframe(obj, at=attr, q=True)
    #print keys
    if preRoll:
        if cmds.setInfinity(obj, at=attr, q=True, pri=True)[0] == 'constant':
            cmds.setInfinity(obj, at=attr, pri='linear')
        preRollFrame = keys[0] - preRollNum
        cmds.setKeyframe(obj, at=attr, insert=True, t=(preRollFrame,preRollFrame))
    if postRoll:
        if cmds.setInfinity(obj, at=attr, q=True, poi=True)[0] == 'constant':
            cmds.setInfinity(obj, at=attr, poi='linear')
        postRollFrame = keys[-1] + postRollNum
        cmds.setKeyframe(obj, at=attr, insert=True, t=(postRollFrame,postRollFrame))


def preRollToDefault(defaultNum, defaultVal, obj, attr):
    keys = cmds.keyframe(obj, at=attr, q=True)
    rollToDefaultFrame = keys[0]-defaultNum
    cmds.setKeyframe(obj, at=attr, t=(rollToDefaultFrame,rollToDefaultFrame), v=defaultVal)


def getSelectionSetMember(rigConfig, targetSet):        
    ctlNs = cmds.ls("*:WEFX_*_*", type='objectSet')
    ctl = cmds.ls("WEFX_*_*", type='objectSet')#if no namespace
    target = ctlNs + ctl

    availableSet = {}

    if target:
        for k in target:
            tag = returnWEFXTag(k)             
            selShape = cmds.listRelatives(k, f=True, ni=True)
            sel = []
            availableSet = {}
            if tag[0] == 'WEFX':
                if tag[1] in rigConfig.keys():                    
                    if '_'.join(tag) == rigConfig[tag[1]][targetSet]:
                        
                        availableSet[k] = {}
                        selShape = cmds.listRelatives(k, f=True, ni=True)
                        sel = []

                        for i in selShape:
                            node = cmds.listRelatives(i, p=True, type='transform', f=True)[0]     
                            if not node in sel:
                                sel.append(node) 
                        availableSet[k]['member'] = sel
                        availableSet[k]['tag'] = tag[1]
                        availableSet[k]['anmNodeType'] =  rigConfig[tag[1]]['anmNodeType']
    
    if availableSet:
        return availableSet
    else:
        return False

def compareValToDefault(val, config):
    pass

def getAvailableAttrs(sel, excludeNode=None):
    attrs = cmds.listAttr(sel, v=True, k=True)
    outAttrs=[]
    for k in attrs:
        connection = cmds.listConnections('%s.%s'%(i,k), s=True, d=False)
        if connection:
            if excludeNode:
                if cmds.objectType(connection[0]) in excludeNode:
                    outAttrs.append(k)
        else:
            outAttrs.append(k)

def getDefaultVal(sel, attr):
    return cmds.attributeQuery(sel, node=sel, ld=True) 

def removeNameSapce(inputData):
    tarData = inputData.split('|') 
    for idx in range(len(tarData)):
        tarData[idx] = tarData[idx].split(':')[-1]
    tarData = '|'.join(tarData)
    return tarData

def swapNameSapce(inputData, namespace):
    tarData = inputData.split('|') 
    for idx in range(len(tarData)):
        tarData[idx] = tarData[idx].split(':')[-1]
        tarData[idx] = namespace + ':' + tarData[idx] 
    tarData = '|'.join(tarData)
    return tarData
