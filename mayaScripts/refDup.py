import maya.cmds as cmds
import os
k = cmds.ls(sl=True,l=True)
referenceN=[]
dupCount = 1

for x in k:
    if cmds.referenceQuery(x,inr=True):
        rfn = cmds.referenceQuery(x,rfn=True)
        if rfn not in referenceN:
            referenceN.append(rfn)
            kFile = cmds.referenceQuery(x, f=True)
            nSpace = os.path.basename(kFile).split('.')[0]
            kNode =  cmds.referenceQuery(x,n=True)
            
            for ci in range(0,dupCount):            
                rK = cmds.file(kFile,r=True,iv=True,gl=True,options='v=0;',namespace=nSpace,mnc=False)
                rKNode = cmds.referenceQuery(rK,n=True)
     
                for i in range(0,len(kNode)-1):
                    if cmds.objectType(kNode[i])=='transform':
                        transV = cmds.getAttr(kNode[i]+'.translate')
                        rotV = cmds.getAttr(kNode[i]+'.rotate')
                        scaleV = cmds.getAttr(kNode[i]+'.scale')                   
                        cmds.setAttr(rKNode[i]+'.translate',transV[0][0], transV[0][1], transV[0][2],type='double3') 
                        cmds.setAttr(rKNode[i]+'.rotate',rotV[0][0], rotV[0][1], rotV[0][2])
                        cmds.setAttr(rKNode[i]+'.scale',scaleV[0][0], scaleV[0][1], scaleV[0][2])
                    
        else:
            pass
    else:
        pass
