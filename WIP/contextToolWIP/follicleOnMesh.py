import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds

ctx = 'myCtx'

def onPress():
    vpX, vpY, _ = cmds.draggerContext(ctx, query=True, anchorPoint=True)
    #print(vpX, vpY)

    pos = om.MPoint()
    dir = om.MVector()
    hitpoint = om.MFloatPoint()
    omui.M3dView().active3dView().viewToWorld(int(vpX), int(vpY), pos, dir)
    pos2 = om.MFloatPoint(pos.x, pos.y, pos.z)
    lm=cmds.ls(sl=True,l=True)
    tarMesh=[]
    for i in lm:
        selMesh=cmds.listRelatives(s=True,type='mesh')
        if selMesh:
            for k in selMesh:
                if not cmds.getAttr('%s.intermediateObject'%k):
                    tarMesh.append(k)
    if not tarMesh:
        tarMesh=[i for i in cmds.ls(type='mesh') if not cmds.getAttr('%s.intermediateObject'%i)]
        
    for mesh in tarMesh:
        selectionList = om.MSelectionList()
        selectionList.add(mesh)
        dagPath = om.MDagPath()
        selectionList.getDagPath(0, dagPath)
        fnMesh = om.MFnMesh(dagPath)
        intersection = fnMesh.closestIntersection(
        om.MFloatPoint(pos2),
        om.MFloatVector(dir),
        None,
        None,
        False,
        om.MSpace.kWorld,
        99999,
        False,
        None,
        hitpoint,
        None,
        None,
        None,
        None,
        None)
        if intersection:
            x = hitpoint.x
            y = hitpoint.y
            z = hitpoint.z
            #print x,y,z
            x1 = om.MScriptUtil()
            x1.createFromList( [0.0,0.0], 2 )
            uvPoint = x1.asFloat2Ptr()            
            fnMesh.getUVAtPoint(om.MPoint(x,y,z),uvPoint,om.MSpace.kWorld)            
            uVal=om.MScriptUtil.getFloat2ArrayItem(uvPoint, 0, 0)
            vVal=om.MScriptUtil.getFloat2ArrayItem(uvPoint, 0, 1)
            
            existLoc=1
            validLoc=cmds.ls(sl=True,l=True)
            if validLoc and cmds.listRelatives(validLoc[0],typ='locator'):
                hC=cmds.listConnections('%s.rotatePivot'%validLoc[0],s=False,d=True)
                #print hC
                if hC:
                    if cmds.objectType(hC[0])=='parentConstraint':
                        folC=cmds.listConnections('%s.target[0].targetTranslate'%hC[0],s=True,d=False)
                        folT=folC[0]
                        existLoc=0
            
            if existLoc:            
                cLoc=cmds.spaceLocator(p=(0,0,0))[0]
                cmds.xform(cLoc,s=[50,50,50])
                meshN=dagPath.fullPathName()
    
                #hSys=cmds.ls(type='hairSystem')[0]
                fol = cmds.createNode('follicle')
                folT=cmds.listRelatives(p=True)[0]
                '''
                idx=cmds.getAttr('%s.inputHair'%hSys,multiIndices=True)
                if idx:
                    idList =sorted([int(i)for i in idx])
                    nextId=idList[-1]+1
                else:
                    nextId=0
                '''
                cmds.connectAttr('%s.outTran   slate'%fol,'%s.translate'%folT)
                cmds.connectAttr('%s.outRotate'%fol,'%s.rotate'%folT)
                
                #cmds.connectAttr('%s.outHair'%fol,'%s.inputHair[%s]'%(hSys,nextId),f=True)
                
                cmds.connectAttr('%s.worldMatrix[0]'%meshN,'%s.inputWorldMatrix'%folT)
                cmds.connectAttr('%s.outMesh'%meshN,'%s.inputMesh'%folT)
                cmds.parentConstraint(folT,cLoc)          
              
            cmds.setAttr('%s.simulationMethod'%folT,0)
            cmds.setAttr('%s.parameterU'%folT,uVal)
            cmds.setAttr('%s.parameterV'%folT,vVal)
            #print folT,cLoc
            return
            
    
                      
if cmds.draggerContext(ctx, exists=True):
    cmds.deleteUI(ctx)
cmds.draggerContext(ctx, pc=onPress, name=ctx, cursor='crossHair')
cmds.setToolTo(ctx)
