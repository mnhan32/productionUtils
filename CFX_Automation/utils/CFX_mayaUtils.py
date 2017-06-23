import maya.cmds as cmds
import os, glob, json

def returnWEFXTag(inputName):
    nspace = cmds.ls(inputName,l=True,sns=True)[1]
    baseName = inputName.split('|')[-1]
    if not nspace == ':':
        baseName = baseName.split(':')[-1]
    baseName = baseName.split('_')
    return baseName

def swapReference(config):
    sceneName = cmds.file(q=True, sceneName=True)
    refs = cmds.file(q=True, r=True)
    print config
    if refs:
        for ref in refs:
            rfn = cmds.referenceQuery(ref, rfn=True)
            fpath = cmds.referenceQuery(rfn, filename=True, wcn=True)
            if cmds.referenceQuery(rfn, il=True):
                print '%s is loaded'%rfn
            else:
                baseRig = os.path.basename(fpath)
                rigName = baseRig.split('_')[0]    #need to fix if naming change
                print rigName
                if rigName in config.keys():
                    print 'MATCH'
                    targetRig = os.path.join(config[rigName]['animRigPath'], baseRig)
                    print targetRig
                    if os.path.isfile(targetRig):
                        print 'REF FILE'
                        cmds.file(targetRig, lr=rfn)
                    return True
                else:
                    print 'config key: %s not existed.'%rigName
                    return False
    else:
        print 'there is no reference existed in file %s'%sceneName
        return False

def exportAnimationNode(outPath, config):
    #export animation node, and json
    ctlNs = cmds.ls("*:WEFX_*_control", type='objectSet')
    ctl = cmds.ls("WEFX_*_control", type='objectSet')#if no namespace
    target = ctlNs + ctl

    #print outPath
    #print target
    
    animationNodeType = ['animCurveTA', 'animCurveTL', 'animCurveTT', 'animCurveTU']
    #config = getJsonObj(configPath, configFile) 
    count = 0
    for k in target:
        count += 1
        animData={}
        nspace = cmds.ls(k,l=True,sns=True)[1]
        if nspace==':':
            nspace = ''                   
        selShape = cmds.listRelatives(k, f=True, ni=True)
        sel = []
        animData['namespace'] = nspace
        tag = returnWEFXTag(k)
        if tag[0] == 'WEFX':
            #print tag
            #print config
            if tag[1] in config.keys():   
                #print 'here2'
                #print '%s.WEFX_version'%k
                version = cmds.getAttr('%s.WEFX_version'%k)     
                     
                animData['targetAsset'] = tag[1]#get name from ctrlset name
                filePattern = '%s_*.%s'%( config[tag[1]]['animRigName'], config[tag[1]]['animRigType'])#need to fix if naming change
                targetPath = os.path.join(config[tag[1]]['animRigPath'],filePattern)
                #print filePattern
                #print targetPath
                fileList = glob.glob(targetPath)
                #print fileList
                animData['targetRigFile'] = sorted(fileList)[-1]
                #print 'HERE'
                if not version == 0:
                    diffVersionFile =  config[tag[1]]['animRigName']+'V%s'%version.zfill(2)+ config[tag[1]]['animRigType']#need to fix if naming change
                    if os.path.isfile(diffVersionFile):
                        animData['targetRigFile'] = diffVersionFile
                
        animData['animCtl'] = {}
        animData['nonKeyCtl'] = {}
        animNodes = []
        #print 'There2'  
        for i in selShape:
            node = cmds.listRelatives(i, p=True, type='transform', f=True)[0]     
            if not node in sel:
                sel.append(node)
                availableAttrs = cmds.listAttr(node, v=True, k=True, u=True)
                #print node, availableAttrs
                if availableAttrs:                
                    for a in availableAttrs:
                        aNode = cmds.listConnections('%s.%s'%(node, a), s=True, d=False, scn=True)                    
                        if aNode:
                            #write connection
                            for n in aNode:                            
                                if cmds.objectType(n) in animationNodeType:   
                                    if not node in animData['animCtl'].keys():
                                        animData['animCtl'][node] = {}      
                                    animData['animCtl'][node][a] = n
                                    animNodes.append(n)                                                        
                        else:
                            #write data
                            currentVal = cmds.getAttr('%s.%s'%(node, a))
                            if not node in animData['nonKeyCtl'].keys():
                                animData['nonKeyCtl'][node] = {}
                            animData['nonKeyCtl'][node][a] = currentVal
        #print 'There4'                    
        cmds.select(sel, r=True)
        if 'animCtl' in animData.keys():
            sceneName = cmds.file(q=True, sceneName=True)
            anmNodeFile = 'anmNode.' + '.'.join(sceneName.split('.')[-3:])
            extFile = os.path.join(outPath, anmNodeFile )
            tmp = 'anmNode.' + '.'.join(sceneName.split('.')[-3:-1]) + '.json'
            extJson = os.path.join(outPath,tmp)
            #print extFile
            #print extJson
            outFile = cmds.file(extFile, force=True, type='mayaAscii',eas=True)
            animData['animFile'] = outFile

        #store output init file path
        initAnmFileName = '.'.join(sceneName.split('.')[-3:]
        animData['outFile'] = os.path.join(outPath,initAnmFileName)

        with open( extJson, 'w') as f:
            json.dump(animData,f)
        return extJson
        print 'finish exporting animation data.'

def generateCleanAnimation(config):
    if os.path.isfile(config['targetRigFile']):
        ref = fName=cmds.file(config['targetRigFile'],r=True,ignoreVersion=True,mergeNamespacesOnClash=False,ns=config['namespace'],options="v=0;")

    if 'animFile' in config.keys():
        cmds.file(config['animFile'], i=True, namespace=":", options="mo=0")
        for i in config['animCtl'].keys():
            for attr in config['animCtl'][i].keys():
                cmds.connectAttr('%s.output'%config['animCtl'][i][attr], '%s.%s'%(i,attr), f=True)

    for i in config['nonKeyCtl'].keys():
        for attr in config['nonKeyCtl'][i].keys():
            cmds.setAttr('%s.%s'%(i,attr), config['nonKeyCtl'][i][attr])


def extendAnimPrePostRoll(selection, attrs, sf, ef, preRollNum, postRollNum, defaultNum, defaultVal):
    for sel in selection:
        for attr in attrs:
            keys = cmds.keyframe(sel, at=attr, q=True)
            if keys:
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
                setPrePostRoll(1,1,preroll,preroll,sel,attr)
                preRollToDefault(defaultNum, defaultVal, sel, attr)
            else:
                sfVal = cmds.getAttr('%s.%s'%(sel,attr))
                if not sfVal == defaultVal:
                    cmds.setKeyframe(sel, at=attr, t=(sf,sf), v=defaultVal)
                    setPrePostRoll(1,0,preroll,preroll,sel,attr)
                    preRollToDefault(defaultNum, defaultVal, sel, attr)
                else:
                    pass


def setPrePostRoll(preRoll, postRoll, preRollNum, postRollNum, obj, attr):
    keys = cmds.keyframe(sel, at=attr, q=True)
    if preRoll:
        if cmds.setInfinity(obj, at=attr, q=True, poi=True)[0] == 'constant':
            cmds.setInfinity(obj, at=attr, poi='linear')
        preRollFrame = keys[0] - preRollNum
        cmds.setKeyframe(obj, at=attr, insert=True, t=(preRollFrame,preRollFrame))
    if postRoll:
        if cmds.setInfinity(obj, at=attr, q=True, poi=True)[0] == 'constant':
            cmds.setInfinity(obj, at=attr, poi='linear')
        postRollFrame = keys[-1] - postRollNum
        cmds.setKeyframe(obj, at=attr, insert=True, t=(postRollFrame,postRollFrame))
    
def preRollToDefault(defaultNum, defaultVal, obj, attr):
    keys = cmds.keyframe(sel, at=attr, q=True)
    rollToDefaultFrame = keys[0]-defaultNum
    cmds.setKeyframe(obj, at=attr, t=(rollToDefaultFrame,rollToDefaultFrame), v=defaultVal)
    

def getSelectionSetMember(config, targetSet):        
    ctlNs = cmds.ls("*:WEFX_*_*", type='objectSet')
    ctl = cmds.ls("WEFX_*_*", type='objectSet')#if no namespace
    target = ctlNs + ctl

    avaiableSet = {}

    if target:
        for k in target:
            tag = returnWEFXTag(k)             
            selShape = cmds.listRelatives(k, f=True, ni=True)
            sel = []
            avaiableSet = {}
            if tag[0] == 'WEFX':
                if tag[1] in config.keys(): 
                    if tag[2] == config[tag[1]][targetSet]:
                        selShape = cmds.listRelatives(k, f=True, ni=True)
                        sel = []

                        for i in selShape:
                            node = cmds.listRelatives(i, p=True, type='transform', f=True)[0]     
                            if not node in sel:
                                sel.append(node) 
                        avaiableSet[k] = sel
    
    if availableSet:
        return avaiableSet
    else:
        return False
    