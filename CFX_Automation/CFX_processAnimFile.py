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
        fileopen =  cmds.file( inputFile, o=True, f=True )
        rigConfig = CFX_utils.getConfig('CFX')
        #print rigConfig
        #swap file      
        swapRef = CFX_mayaUtils.swapReference(rigConfig)
        if not swapRef:
            print 'swap ref failed on %s'%fileopen
            return False
        print 'finish swap'
        #get to project anim folder
        tarFolder = os.path.join(result['anmPath'],'work')
        tarFolder = os.path.join(tarFolder, 'maya')        
        tarFile = os.path.join(tarFolder, 'outsource.'+'.'.join(inputFile.split('.')[-3:]))
        print 'tar : %s'%tarFile
        #save to anim folder after swap
        if os.path.isfile(tarFile):
            print 'file already exist.'
            return False
        cmds.file(rename = tarFile)
        cmds.file(s=True, f=True, typ='mayaAscii')
        print 'animation file saved'

        #extExport animation node
        jsonFile = CFX_mayaUtils.exportAnimationNode(tarFolder, rigConfig)
        print 'export animation node finished'


        #create clean animation file
        anmData = CFX_utils.getConfig(jsonFile,tarFolder)     
        cmds.file(new=True)
        CFX_mayaUtils.generateCleanAnimation(anmData)
        cmds.file(rename = anmData['outFile'])
        cmds.file(s=True, f=True, typ='mayaAscii')        
        print 'finish creating init animation file'
        
        #extend animation for CFX
        CFX_mayaUtils.extendAnimPrePostRoll()
        
        
        cmds.quit()

        print 'Finished swapping reference for %s'%fileName
    except:
        print 'Failed swapping reference for %s'%fileName
        return False

if __name__ == '__main__':
    inputAnime = sys.argv[1]
    main(inputAnime)
    sys.exit()