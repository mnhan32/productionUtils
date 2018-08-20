import maya.cmds as cmds
import time,math

cLoc = ''
cPos = []
dPos = []
nNode = []

def rad2deg(radians):
	pi = math.pi
	degrees = 180 * radians / pi
	return degrees

def SampleContextDrag(dCtx,tar,source):
        modifier = cmds.draggerContext(dCtx, query=True, modifier=True)
        print 'drag: ', modifier
        cmds.makeLive(tar)
        global cLoc,cPos,dPos,nNode
        pPos = cmds.autoPlace(um=True)

        if modifier =='none':
            cPos = pPos
            dPos = cmds.draggerContext( dCtx, q=True, dragPoint=True)
            cmds.move(pPos[0],pPos[1],pPos[2],cLoc,a=True)
            cmds.normalConstraint(tar, cLoc)

        elif modifier =='ctrl':
            disPos = cmds.draggerContext( dCtx, q=True, dragPoint=True)
            dis0 = dPos[0] - disPos[0]
            dis1 = dPos[1] - disPos[1]

            cmds.normalConstraint(tar, cLoc)
            cmds.xform(cLoc,ro=[rad2deg(dis1*0.1),0,rad2deg(dis0*0.1)],r=True,os=True)
        elif modifier =='shift':
            disPos = cmds.draggerContext( dCtx, q=True, dragPoint=True)
            dis0 = dPos[0] - disPos[0]
            cmds.xform(cLoc,scale=[dis0*.5+1.0,dis0*.5+1.0,dis0*.5+1.0],a=True)
        elif modifier =='other':
            disPos = cmds.draggerContext( dCtx, q=True, dragPoint=True)
            dis0 = dPos[0] - disPos[0]
            cmds.normalConstraint(tar, cLoc)
            cmds.xform(cLoc,ro=[0,rad2deg(dis0*0.1),0],r=True,os=True)
        cmds.refresh()

def SampleContextPrePress(dCtx,tar,source):
        print 'pre-press'

def SampleContextPress(dCtx,tar,source):
        print 'press'
        cmds.makeLive(tar)
        s1 = cmds.polyCone()
        global cLoc,cPos,dPos,nNode
        dPos = cmds.draggerContext( dCtx, q=True, dragPoint=True)
        cLoc = s1[0]
        cPos = cmds.autoPlace(um=True)
        cmds.move(cPos[0],cPos[1],cPos[2],cLoc,a=True)
        cmds.normalConstraint(tar, cLoc, aim=[0,1,0])
        time.sleep(0.1)
        cmds.refresh()

def exitContext():
        cmds.makeLive(n=True)
        print 'end'

def releaseContext():
       print 'release'
       global nNode
       for i in nNode:
           cmds.delete(i)

sel = cmds.ls(sl=True,l=True)
tar = sel[0]

dCtx = 'myDragger'
try:
    if cmds.draggerContext(dCtx,exists=True,q=True):
        cmds.deleteUI(dCtx)
except:
    pass

cmds.draggerContext(dCtx,cursor='hand',finalize='exitContext()',dragCommand='SampleContextDrag("'+dCtx+'","'+tar+'","'+source+'")',pressCommand='SampleContextPress("'+dCtx+'","'+tar+'","'+cLoc+'")',releaseCommand='releaseContext()',prePressCommand='SampleContextPrePress("'+dCtx+'","'+tar+'","'+cLoc+'")',sp='world',pr='objectViewPlane')
cmds.setToolTo(dCtx)
