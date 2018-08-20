import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds

ctx = 'myCtx'

def onPress():
    vpX, vpY, _ = cmds.draggerContext(ctx, query=True, anchorPoint=True)
    print(vpX, vpY)

    pos = om.MPoint()
    dir = om.MVector()
    hitpoint = om.MFloatPoint()
    omui.M3dView().active3dView().viewToWorld(int(vpX), int(vpY), pos, dir)
    pos2 = om.MFloatPoint(pos.x, pos.y, pos.z)
    for mesh in cmds.ls(type='mesh'):
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
            cLoc=cmds.spaceLocator(p=(x,y,z))
            intersectMesh=dagPath.fullPathName()
            tar=cmds.listRelatives(intersectMesh,p=True)[0]
            mNormal=om.MVector()
            fnMesh.getClosestNormal(om.MPoint(x,y,z),mNormal,om.MSpace.kWorld)
            print mNormal.x,mNormal.y,mNormal.z
            k=om.MQuaternion()
            k.MQuaternion(om.MVector(0,1,0),mNormal)
            print k.x,k.y,k.z
    

if cmds.draggerContext(ctx, exists=True):
    cmds.deleteUI(ctx)
cmds.draggerContext(ctx, pressCommand=onPress, name=ctx, cursor='crossHair')
cmds.setToolTo(ctx)