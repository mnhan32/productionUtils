import maya.cmds as cmds
outC=cmds.listConnections('time1.outTime',d=True, s=False,p=True)
inW=cmds.listConnections('time1.timewarpIn_Raw',s=True, d=False)

outTL=cmds.ls(type='animCurveTL')
outTA=cmds.ls(type='animCurveTA')
outTU=cmds.ls(type='animCurveTU')
outTT=cmds.ls(type='animCurveTT')
outAnimCurve=outTL+outTA+outTU
#outAnimCurve=cmds.ls(type='animCurve')

if outAnimCurve:
    for ac in outAnimCurve:
        cmds.connectAttr(inW[0]+'.output',ac+'.input',f=True)

if outC:
    for i in outC:
        #print i
        cmds.disconnectAttr('time1.outTime',i)
        cmds.connectAttr(inW[0]+'.output',i,f=True)
