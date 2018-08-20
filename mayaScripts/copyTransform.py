import maya.cmds as cmds

def copyTransformAttr(sel, mode):
    sizeSel = len(sel)
    if sizeSel >1:
        transV = cmds.getAttr(sel[sizeSel-1]+'.translate')
        rotV = cmds.getAttr(sel[sizeSel-1]+'.rotate')
        scaleV = cmds.getAttr(sel[sizeSel-1]+'.scale')
        #print transV,rotV ,scaleV
        print sizeSel-2
        for i in range(0,sizeSel-1):
            print sel[i]
            if mode[0]:
                cmds.setAttr(sel[i]+'.translate',transV[0][0], transV[0][1], transV[0][2],type='double3')
            if mode[1]:
                cmds.setAttr(sel[i]+'.rotate',rotV[0][0], rotV[0][1], rotV[0][2])
            if mode[2]:
                cmds.setAttr(sel[i]+'.scale',scaleV[0][0], scaleV[0][1], scaleV[0][2])

sel = cmds.ls(l=True,sl=True)
modeList = [1,1,1]
copyTransformAttr(sel,modeList)
