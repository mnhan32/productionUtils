import maya.cmds as cmds
import time,math,os

cLoc = ''
cPos = []
dPos = []
nNode = []
mGroup = 'DISGROUP'
cCount=0
fName=''
gCons=[]
def rad2deg(radians):
	pi = math.pi
	degrees = 180 * radians / pi
	return degrees
	
def SampleContextDrag(dCtx,tar,source):
        modifier = cmds.draggerContext(dCtx, query=True, modifier=True)
        print 'drag: ', modifier
        #cmds.makeLive(tar)
        global cLoc,cPos,dPos,nNode,gCons
        pPos = cmds.autoPlace(um=True)
        
        if modifier =='none':
            
            cPos = pPos
            dPos = cmds.draggerContext( dCtx, q=True, dragPoint=True)
            cmds.move(pPos[0],pPos[1],pPos[2],cLoc,a=True)
            nNode += cmds.normalConstraint(tar, cLoc)

        elif modifier =='ctrl':

            disPos = cmds.draggerContext( dCtx, q=True, dragPoint=True)
            dis0 = dPos[0] - disPos[0]
            dis1 = dPos[1] - disPos[1]
            nNode += cmds.normalConstraint(tar, cLoc)
            cmds.xform(cLoc,ro=[rad2deg(dis1*0.1),0,rad2deg(dis0*0.1)],r=True,os=True)
        elif modifier =='shift':
            disPos = cmds.draggerContext( dCtx, q=True, dragPoint=True)
            dis0 = dPos[0] - disPos[0]
            cmds.xform(cLoc,scale=[dis0*.5+1.0,dis0*.5+1.0,dis0*.5+1.0],a=True)    
        elif modifier =='other':
            
            disPos = cmds.draggerContext( dCtx, q=True, dragPoint=True)
            dis0 = dPos[0] - disPos[0]
            nNode += cmds.normalConstraint(tar, cLoc)
            cmds.xform(cLoc,ro=[0,rad2deg(dis0*0.1),0],r=True,os=True)
        cmds.refresh()



def SampleContextPrePress(dCtx,tar,source,mode):  
        print 'pre-press'
        global cLoc,cPos,dPos,nNode,mGroup
        #if not cmds.objExists(mGroup):
            #cmds.group(n=mGroup)
        #print 'a', source
        #global cLoc,cPos,dPos,nNode
        #
        #print cLoc

def SampleContextPress(dCtx,tar,source,mode):
        print 'press'
        
        global cLoc,cPos,dPos,nNode,mGroup,cCount,fName,gCons
        #if cLoc:
            #cmds.parent(cLoc,mGroup)
        if source:    
            if os.path.isfile(os.path.abspath(source)):
                print 'here2'
                fName = source
            else:
               if cmds.objExists(source):
                   try:
                       rfn = cmds.referenceQuery(source,rfn=True)
                       if rfn:
                           fName = cmds.referenceQuery(source,f=True)
                   except:
                       fName=''          
            if fName:
                cLoc = cmds.spaceLocator()[0]
                #print 'TTT', fName
                #nN = cmds.file(fName,r=True,iv=True,gl=True,options='v=0;',namespace=('layoutObj'+str(cCount)),mnc=False)
                #cCount +=1
                #cLoc = cmds.referenceQuery(nN,n=True,dp=True)[0]
                
            else:
                
                print 'here0'
                if cmds.objExists(source):               
                    if mode=='copy':
                        cLoc = cmds.duplicate(source,rr=True)
                    else:
                        cLoc = cmds.instance(source)
                else:
                    print 'here1'
                    cLoc = cmds.spaceLocator()[0]
        else:
            print 'here1'
            cLoc = cmds.spaceLocator()[0]
        
        cmds.makeLive(tar)
        dPos = cmds.draggerContext( dCtx, q=True, dragPoint=True)
        cPos = cmds.autoPlace(um=True)
        cmds.move(cPos[0],cPos[1],cPos[2],cLoc,a=True)
        cons = cmds.normalConstraint(tar, cLoc, aim=[0,1,0])
        nNode +=cons
        cmds.refresh()

def exitContext():
        cmds.makeLive(n=True)
        print 'end'

def releaseContext():
       print 'release'
       global nNode,gCons,fName,cLoc,mGroup
       if fName:
           nN = cmds.file(fName,r=True,iv=True,gl=True,options='v=0;',namespace=('layoutObj'+str(cCount)),mnc=False)   
           copyTransformAttr([cmds.referenceQuery(nN,n=True,dp=True)[0],cLoc],[1,1,1])
           cmds.delete(cLoc)
           cLoc = cmds.referenceQuery(nN,n=True,dp=True)[0]
       for i in nNode:
           #print i
           if cmds.objExists(i):
               #pass
               cmds.delete(i)
       print 'group here'
       if not cmds.objExists(mGroup):
           cmds.select(cl=True)
           cmds.group(n=mGroup,w=True,em=True)
           
       cmds.parent(cLoc,mGroup,r=True)
               
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
sel = cmds.ls(sl=True,l=True)   
tar = sel[0]
cMode='copy'

source = "C:\Users\mnhan\Documents\maya\projects\default\scenes\source.ma"

if len(sel)>1:   
    source = sel[1]


#


dCtx = 'myDragger'
try:
    if cmds.draggerContext(dCtx,exists=True,q=True):
        cmds.deleteUI(dCtx)
except:
    pass
print source
cmds.draggerContext(dCtx,cursor='hand',finalize='exitContext()',dragCommand='SampleContextDrag("'+dCtx+'","'+tar+'","'+cLoc+'")',pressCommand='SampleContextPress("'+dCtx+'","'+tar+'","'+source+'","'+cMode+'")',releaseCommand='releaseContext()',prePressCommand='SampleContextPrePress("'+dCtx+'","'+tar+'","'+source+'","'+cMode+'")',sp='world',pr='objectViewPlane')
cmds.setToolTo(dCtx)

