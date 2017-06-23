#require maya standalong
try:
    import maya.standalone 
    maya.standalone.initialize(name='python') 
except: 
    pass
import os,sys, time 
import maya.cmds as cmds

import json, glob
from utils import CFX_utils, CFX_mayaUtils, CFX_shotgunInfo

def main(inputFile):
    #file open 
    fileName = os.path.basename(inputFile)
    #print fileName
    result = CFX_shotgunInfo.shotgunInfo(fileName)
    if 'err' in result.keys():
        print result['err']
        return False
    try:
        #open file in maya        
        config = CFX_utils.getConfig('proj')
        rigConfig = CFX_utils.getConfig('CFX')

        #get to project anim folder
        tarFolder = os.path.join(result['anmPath'],'work')
        tarFolder = os.path.join(tarFolder, 'maya')        
        tarFile = os.path.join(tarFolder, 'outsource.'+'.'.join(inputFile.split('.')[-3:]))

        print 'tar : %s'%tarFile
        #save to anim folder after swap
        if os.path.isfile(tarFile):
            print 'file already exist.'
            fileopen =  cmds.file( tarFile, o=True, f=True )
        else:
            fileopen =  cmds.file( inputFile, o=True, f=True )
            #swap file      
            swapRef = CFX_mayaUtils.swapReference(rigConfig)
            if not swapRef:
                print 'swap ref failed on %s'%fileopen
                return False
            else:
                print 'finish swap'        
                cmds.file(rename = tarFile)
                cmds.file(s=True, f=True, typ='mayaAscii')
                print 'animation file saved'
        
        #currently in shot folder
        sceneName = cmds.file(q=True, sceneName=True)
        currentDir = os.path.dirname(sceneName)
        anmNodeFile = 'anmNode.' + '.'.join(sceneName.split('.')[-3:])
        jsonNodeFile = 'anmNode.' + '.'.join(sceneName.split('.')[-3:-1]) + '.json'
        initAnmFileName = '.'.join(sceneName.split('.')[-3:])
        initAnmFilePath = os.path.join(currentDir,initAnmFileName)
        #extExport animation node
        print 'here2'
        print anmNodeFile, jsonNodeFile
        if not os.path.isfile(anmNodeFile) and not os.path.isfile(jsonNodeFile):
            print 'here'
            jsonFile = CFX_mayaUtils.exportAnimationNode(tarFolder, rigConfig, 'ctrlSet')

            print 'export animation node finished'


        #create clean animation file
        anmData = CFX_utils.getConfig(jsonFile,tarFolder)
        if os.path.isfile(initAnmFilePath):
            print 'init animation file existed.'
            fileopen =  cmds.file(initAnmFilePath, o=True, f=True )
        else:
            cmds.file(new=True)
            CFX_mayaUtils.generateCleanAnimation(anmData)
            cmds.file(rename = initAnmFilePath)
            cmds.file(s=True, f=True, typ='mayaAscii')        
            print 'finish creating init animation file'
        

        #extend animation for CFX
        '''
        availableSet = CFX_mayaUtils.getSelectionSetMember(rigConfig, 'ctrlSet')
        tmpF = os.path.basename(animData['targetRigFile'])
        tmpP = os.path.dirname(animData['targetRigFile'])
        tmpJ = '.'.join(tmpF.split('.')[0:-1]) + '.json'
        defaultJson
        for k in availableSet:                        
            CFX_mayaUtils.extendAnimPrePostRoll(availableSet[k]['member'], result['head_in'], result['tail_out'],config['project']['preRoll'],config['project']['postRoll'],config['project']['rollTpoDefault'])
        '''
        
        
        cmds.quit()

        print 'Finished animation init setup for %s'%fileName
    except:
        print 'Failed animation init setup for %s'%fileName
        return False

if __name__ == '__main__':
    inputAnime = sys.argv[1]
    main(inputAnime)
    sys.exit()