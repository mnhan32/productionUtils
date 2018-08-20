import maya.cmds as cmds
import maya.mel as mel
import re

sel=cmds.ls(sl=True,fl=True)
mAmt=0.2
for i in sel:
    ver='%s.vtx[0:]'%i   
    cmds.select(ver)
    vv=int(re.findall('\d+',cmds.ls(sl=True)[0].split(':')[1])[0])    
    narg=''
    for k in range(vv+1):
        narg=narg+' -n %s'%mAmt
    mel.eval('moveVertexAlongDirection%s'%narg)
