import maya.cmds as cmds
sel=cmds.ls(sl=True,l=True)
for x in sel:
    cPos = cmds.xform(x,a=True,ws=True)
    bbox = cmds.exactWorldBoundingBox(x)
    newPivotRoot=[(bbox[3]-bbox[0])*.5+bbox[0],bbox[1],(bbox[5]-bbox[2])*.5+bbox[2]]
    cmds.xform(x,a=True,ws=True,piv=newPivotRoot)
