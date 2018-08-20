import maya.cmds as cmds

sel=cmds.ls(sl=True,l=True)
qFrame=597
for i in sel:
    print cmds.keyframe( query=True,q=True, ev=True,time=(qFrame,qFrame))