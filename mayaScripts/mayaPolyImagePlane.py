import maya.cmds as cmds

#when distSwitch is 0, script will ignore imageplane, use polyplane z transition instead
distSwitch=0

#calculate h/w ratio
w=float(cmds.getAttr('defaultResolution.width'))
h=cmds.getAttr('defaultResolution.height')
r=h/w

#for each camera selected
for i in cmds.ls(sl=True,l=True):
    
    #get camera shape and shortname
    camShape=cmds.listRelatives(i,type='camera')
    sName=cmds.ls(i)
    #if selection is camera
    if camShape:
        #get imageplane
        iPlaneT=cmds.listConnections(camShape[0]+'.imagePlane[0]',s=True,d=False)
        if iPlaneT and distSwitch:
            iPlane=cmds.listRelatives(iPlaneT[0])
        else:
            #if there is no imageplane or distSwitch is 0
            iPlane=None
            iPlaneT=None

        #create projection plane
        pPlane=cmds.polyPlane(sx=1,sy=1,w=1,h=r,n=sName[0]+'_PLOYPLANE')
        #in case autoreane after parent poly plane into camera
        pPlane=cmds.parent(pPlane[0],i)
        cmds.setAttr(pPlane[0]+'.translate',0,0,0,type='double3')
        cmds.setAttr(pPlane[0]+'.rotate',90,0,0,type='double3')
        cmds.setAttr(pPlane[0]+'.scale',1,1,1,type='double3')

        if iPlane:      
            #reverse dist
            mD=cmds.createNode('multiplyDivide')
            cmds.setAttr(mD+'.input2X',-1)
            cmds.connectAttr(iPlane[0]+'.depth', mD+'.input1X')
        
        #aperture inch to mm
        mD1=cmds.createNode('multiplyDivide')
        cmds.setAttr(mD1+'.input2X',25.4)
        cmds.connectAttr(camShape[0]+'.horizontalFilmAperture', mD1+'.input1X')
        
        #dist / focalLength
        mD2=cmds.createNode('multiplyDivide')
        cmds.setAttr(mD2+'.operation',2)
        
        if iPlane:  
            cmds.connectAttr(iPlane[0]+'.depth', mD2+'.input1X')
        else:
            cmds.connectAttr(pPlane[0]+'.tz', mD2+'.input1X')
            
        cmds.connectAttr(camShape[0]+'.focalLength', mD2+'.input2X')
        
        #aperture*abs(dist/focalLength)
        mD3=cmds.createNode('multiplyDivide')
        cmds.connectAttr(mD1+'.outputX', mD3+'.input1X')
        cmds.connectAttr(mD2+'.outputX', mD3+'.input2X')
        
        #connect to imagePlane
        cmds.connectAttr(mD3+'.outputX',pPlane[0]+'.scaleX')
        cmds.connectAttr(mD3+'.outputX',pPlane[0]+'.scaleZ')
        
        if iPlane:
            cmds.connectAttr(mD+'.outputX',pPlane[0]+'.translateZ')
    else:
        cmds.warning('%s is not a camera transform node.'%i)
