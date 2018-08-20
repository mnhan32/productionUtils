import maya.cmds as cmds

sel=cmds.ls(sl=True,l=True)
inW=cmds.listConnections('time1.timewarpIn_Raw',s=True, d=False)[0]

for i in sel:
    #expression
    exp=cmds.listConnections(type='expression')
    if exp:
        exp=sorted(set(exp))
        for e in exp:
            cmds.connectAttr(inW+'.output',e+'.time',f=True)
       
    #animCurve except animCurveTT
    his=cmds.listConnections(type='animCurve')
    if his:
        for t in his:
            if cmds.objectType(t)!='animCurveTT':
                cmds.connectAttr(inW+'.output',t+'.input',f=True)
            
