#argparse is not built-in in Python2.6, but MayaPy include it
#require maya standalong
try:
    import maya.standalone 
    maya.standalone.initialize(name='python') 
except:
    pass

import maya.cmds as cmds
import argparse, os, sys, time, json, glob
from utils import CFX_utils, CFX_mayaUtils, CFX_shotgunInfo

def main(args):
    config = CFX_utils.getConfig('proj')
    rigConfig = CFX_utils.getConfig('CFX')
    sourceFilePath = args.s
    sourceFileName = os.path.basename(sourceFilePath)
    tarFolder = args.d
    tarFileName = args.f    
    sourceFileData = sourceFileName.split('_')
    tarFileData = tarFileName.split('_')
    sFrame = int(args.sf)
    eFrame = int(args.ef)
    extraArgument = args.ex.split(' ')
    outSourceFileList = tarFileData
    outSourceFileList.insert(-1, 'outsource')
    outsourceFile = '_'.join(outSourceFileList)
    tarOutSourceFile = os.path.join(tarFolder, outsourceFile)

    initAnmFileName = tarFileName
    initAnmFilePath = os.path.join(tarFolder, tarFileName)

    ###########
    #fileOpen
    print 'CFX AUTOMATION : open file %s'%sourceFilePath
    fileopen =  cmds.file(sourceFilePath, o=True, f=True)
    

    ############################
    #Swap Reference
    print 'CFX AUTOMATION : Swap ref file'
    swapRef = CFX_mayaUtils.swapReference(rigConfig)
    if not swapRef:
        print 'CFX AUTOMATION : swap ref failed on %s'%fileopen
        return False
    else:        
        cmds.file(rename = tarOutSourceFile)
        cmds.file(s=True, f=True, typ='mayaAscii')
        print 'CFX AUTOMATION : Save outsource file %s'%tarOutSourceFile
        print 'CFX AUTOMATION : finish swapping reference'


    ##########################
    #Export Animation Node
    print 'CFX AUTOMATION : Exporting Animation Data'
    sceneName = cmds.file(q=True, sceneName=True)
    currentDir = os.path.dirname(sceneName)
    anmNodeFileList = tarFileData
    anmNodeFileList.insert(-1, 'anmNode')
    anmNodeFile = '_'.join(anmNodeFileList)
    jsonNodeFile = '.'.join(anmNodeFile.split('.')[:-1])+'.json'
    jsonFile = CFX_mayaUtils.exportAnimationNode(tarFolder, rigConfig, anmNodeFile, jsonNodeFile,  'ctrlSet', sFrame, eFrame)
    
    anmData = CFX_utils.getConfig(jsonFile,tarFolder)

    if not anmData:
        print 'CFX AUTOMATION  :no avialble control set in file'
        return False
    else:
        print 'CFX AUTOMATION : Finish exporting animation data'

    #################################
    #Generate Clean Animation file
    print 'CFX AUTOMATION : Generate Clean Init Animation File'
    cmds.file(new=True, f=True)
    CFX_mayaUtils.generateCleanAnimation(anmData)
    cmds.file(rename = initAnmFilePath)
    cmds.file(s=True, f=True, typ='mayaAscii')
    print 'CFX AUTOMATION : save file %s'%initAnmFilePath
    print 'CFX AUTOMATION : Finish creating init animation file'


    #########################
    #extend animation for CFX
    print "CFX AUTOMATION : Animation Extendsion for CFX"
    availableSet = CFX_mayaUtils.getSelectionSetMember(rigConfig, 'ctrlSet')
    
    if not availableSet:
        print 'CFX AUTOMATION :There is no avaible control set for extending animation'
        return False

    if sFrame == 0 and eFrame == 0:
        sFrame = cmds.playbackOptions(q=True, minTime=True)
        eFrame = cmds.playbackOptions(q=True, maxTime=True)

    for k in availableSet: 
        tag =  availableSet[k]['tag']
        print 'CFX AUTOMATION : Found control set %s'%tag
        print 'CFX AUTOMATION : Processing...'
        tmpP = rigConfig[tag]['animRigPath']
        tmpJ = rigConfig[tag]['animRigName']
        fType = rigConfig[tag]['animRigType']

        #get latest rig file
        filePattern  =tmpJ + '.v*.'+fType
        tarRigFile = sorted(glob.glob(os.path.join(tmpP, filePattern)))[-1]
        tarJsonPath = os.path.dirname(tarRigFile)
        tarJsonBase = os.path.basename(tarRigFile)
        tarJson = '.'.join(tarJsonBase .split('.')[0:-1])+'.json'
        jsonFile = CFX_utils.getConfig(tarJson, tarJsonPath)
        if not jsonFile:
            jsonFile = None
            print 'CFX AUTOMATION : No valid default val file exist for %s, use attr default'%tarJsonBase          
        
        CFX_mayaUtils.extendAnimPrePostRoll( availableSet[k]['member'], jsonFile, sFrame, eFrame, config['project']['preRoll'], config['project']['preRollHold'], config['project']['cfxPreRollOffset'], config['project']['cfxPreRoll'], config['project']['postRoll'],config['project']['rollToDefault'])
        extendedStartFrame = sFrame - config['project']['preRoll'] - config['project']['preRollHold'] - config['project']['cfxPreRoll'] - config['project']['rollToDefault']
        extendedEndFrame = eFrame + config['project']['postRoll'] 
    cmds.playbackOptions(ast=extendedStartFrame, aet=extendedEndFrame, minTime=extendedStartFrame, maxTime=extendedEndFrame)

    currentFilePath = cmds.file(q=True,sn=True)
    extendedFileFolder = os.path.dirname(currentFilePath)
    extendedFileName = os.path.basename(currentFilePath)
    #print 'TMP : %s'%extendedFileName
    extendedFile= extendedFileName.split('_')
    extendedFile.insert(-1, 'extened')
    extendedFileName = '_'.join(extendedFile)
    #print 'TMP : %s'%extendedFileName
    extendedFilePath = os.path.join(extendedFileFolder, extendedFileName)
    cmds.file(rename = extendedFilePath)
    cmds.file(s=True, f=True, typ='mayaAscii')
    print 'CFX AUTOMATION : Save file %s'%extendedFilePath
    ####################
    # publish ma file

    ###################
    # publish abc

    print 'CFX AUTOMATION : Finish Extending Animation for CFX.'

    cmds.quit()


if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description = 'Process input arguments.')
    parser.add_argument('-s', help='Maya Scene Name')
    parser.add_argument('-f', help='Output File Name')
    parser.add_argument('-d', help='Output Folder Name')
    parser.add_argument('-sf', help='Start Frame')
    parser.add_argument('-ef', help='End Frame')
    parser.add_argument('-ex', help='Extra Argument String')
    args = parser.parse_args()
    #print args
    main(args)