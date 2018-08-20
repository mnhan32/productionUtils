
#unique rename

import maya.cmds as cmds

item = cmds.ls()
for i in item: 
    if '|' in i:
       print i



import maya.cmds as cmds

def recursiveRenameDup(max):
    while True:   
        limit = len([i for i in cmds.ls(type='transform') if '|' in i])
        if limit == 0:
            break
            
        if max > 0:
            max -= 1
        else:
            break  
              
        item = cmds.ls(type='transform',fl=True)
        for i in item:
            k = cmds.ls(i)[0]
            if '|' in k:
                baseName = k.split('|')[-1]
                ret = cmds.rename(i,'%s#'%baseName)
                print '%s -> %s'%(k,ret)
                break

max = len([i for i in cmds.ls(type='transform') if '|' in i])
recursiveRenameDup(max)
    
