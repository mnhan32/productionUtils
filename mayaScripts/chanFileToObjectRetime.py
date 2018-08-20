import maya.cmds as cmds
import re

sel = cmds.ls(sl=True,l=True)
loc = cmds.spaceLocator()[0]
loc = cmds.rename(loc, 'chainImport')

#chan file source
chanFile = 'Y:\TGB\sequences\demo\demo_0030\Comp\publish\elements\demo_0030.retime.v02.chan';
f = open(chanFile, 'r')

#reformat chan data into array
data=[]
for idx, line in enumerate(f):
    cleanData = re.sub("\r\n", "", line)
    splitData = cleanData.split('\t')
    data.append(splitData)

#read array
for i in data:
    #subject to change how to map value
    #round
    i = [round(float(k)) for k in i]
    #print 'Frame : %s , tx: %s, ty: %s, tz: %s, rx: %s, ry: %s, rz: %s'%(i[0],i[1],i[2],i[3],i[4],i[5],i[6])   
    cmds.setKeyframe( loc, at='tx', time=(i[0],i[0]), v=i[1])
 

#connect 
inW=cmds.listConnections('%s.tx'%loc,s=True, d=False)[0]
print inW


for i in sel:
    #expression
    exp=cmds.listConnections(sel[0],type='expression')
    if exp:
        exp=sorted(set(exp))
        for e in exp:
            cmds.connectAttr(inW+'.output',e+'.time',f=True)
     
    #animCurve except animCurveTT
    his=cmds.listConnections(sel[0],type='animCurve')
    
    if his:
        for t in his:
            print his, t
            if cmds.objectType(t)!='animCurveTT':
                cmds.connectAttr(inW+'.output',t+'.input',f=True)
cmds.delete(loc)
