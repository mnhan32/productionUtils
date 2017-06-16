#if key#
#    if only one
#        if not val == default    
#            set key preroll in out,
#            transition to default 24 frames ahead
#
#    if more than one
#        get the first key
#        if not heads in,  
#            break first key tagent, set heads in key with the same val
#        set key preroll
#        transition to default 24 frames ahead
#
#        get the last key
#        if not tails out,  
#            break first key tagent, set heads in key with the same val
#        set key postroll
#        
#
#if no key
#    check val
#    if not val == default    
#        set key preroll in out,
#        transition to default 24 frames ahead
try:
    import maya.standalone 
    maya.standalone.initialize(name='python') 
except: 
    pass
    
import maya.cmds as cmds
import os,sys, time
import json


def main(inputAnime, configPath):
    #file open 
    try:
        result = cmds.file(inputAnime, o=True, f=True )
        
        basename = '.'.join(os.path.basename(args[1]).split('.')[0:-1])+'.json'
        
        if args[2].upper() == 'DEFAULT':
            mayaFileFolder = os.path.dirname(args[1])
            tarJson = os.path.join(mayaFileFolder, basename)
            print tarJson
        else:
            if os.path.isdir(args[2]):            
                tarJson = os.path.join(args[2], basename)
            else:
                print 'Failed target folder for json is not existed'
                raise
        
        generateDefault(args[1], tarJson, args[3])
        cmds.quit(force=True)
        print 'Finished generate default json for %s'%args[1]
        
    except:
        print 'Failed generate json file for %s'%args[1]
        
    exit()

if __name__ == '__main__':
    inputAnime = sys.argv[1]
    configPath = os.path.dirname(os.path.abspath(__file__))
    main(inputAnime, configPath)