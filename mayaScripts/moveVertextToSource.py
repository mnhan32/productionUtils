import maya.OpenMaya as OpenMaya
def moveVertexToSource():
    mSelList = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(mSelList)
    targetPath = OpenMaya.MDagPath()
    sourcePath = OpenMaya.MDagPath()
    mSelList.getDagPath(0, sourcePath)
    mSelList.getDagPath(1, targetPath)
    sourceMesh = OpenMaya.MFnMesh(sourcePath)
    targetMesh = OpenMaya.MFnMesh(targetPath)
    sourceP = OpenMaya.MPointArray()
    sourceMesh.getPoints(sourceP,OpenMaya.MSpace.kObject)
    targetMesh.setPoints(sourceP,OpenMaya.MSpace.kObject)

moveVertexToSource()
