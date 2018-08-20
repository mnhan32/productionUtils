#Maya Python API 2.0
import maya.api.OpenMaya as om

sel = om.MGlobal.getActiveSelectionList()
mesh = sel.getDagPath(sel.length()-1)
meshNode = sel.getDependNode(sel.length()-1)
iterSelList = om.MItSelectionList(sel)
iterSelList.setFilter(om.MFn.kNurbsCurve)
iterSelList.reset()

intersector = om.MMeshIntersector()
meshNode = mesh.node()
meshMatrix = mesh.inclusiveMatrix()
status = intersector.create(meshNode, meshMatrix)
if status:
    print 'yahoo'
    
    while not iterSelList.isDone():
        pnt = om.mPoint()
        pntOnMesh = om.MPointOnMesh()
        nCurve = iterSelList.getDagPath()
    
    
    
    iterSelList.next()
