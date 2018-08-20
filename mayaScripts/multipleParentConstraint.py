import maya.cmds as cmds
sel=cmds.ls(sl=True,l=True)
for i in sel[0:-1]:
    cmds.parentConstraint(sel[-1],i,mo=True)
