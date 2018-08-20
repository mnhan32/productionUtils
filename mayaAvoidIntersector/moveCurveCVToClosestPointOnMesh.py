#Maya Python API 2.0
import maya.api.OpenMaya as om
import maya.cmds as cmds
import time
tick = time.clock()
sel = om.MGlobal.getActiveSelectionList()
mesh = sel.getDagPath(sel.length()-1)
fnMesh = om.MFnMesh(mesh)
iterSelList = om.MItSelectionList(sel)
iterSelList.setFilter(om.MFn.kNurbsCurve)
iterSelList.reset()

while not iterSelList.isDone():
    curvePath = iterSelList.getDagPath()
    iMatrix = curvePath.inclusiveMatrix()
    iIMatrix = curvePath.inclusiveMatrixInverse()
    fnCurve = om.MFnNurbsCurve(iterSelList.getDependNode())
    knts = fnCurve.knots()
    cvPos = fnCurve.cvPositions()
    cvs = om.MPointArray()
    for idx, i in enumerate(cvPos):
        #object space to worldspace, worldpos = localpos * inclusive matrix      
        wPnt = i*iMatrix
        #print idx, wPnt
        pN = fnMesh.getClosestPointAndNormal(wPnt, space=om.MSpace.kWorld)        
        vecToPnt = om.MVector(wPnt[0]-pN[0][0], wPnt[1]-pN[0][1], wPnt[2]-pN[0][2]).normalize()        
        dotP = vecToPnt*pN[1]#if dot product < 0, point is inside of mesh
        #print dotP
        
        if idx > 2:
            #start index knot
            pass
            
        if dotP < 0:
            #print idx
            #object space to worldspace, localpos = worldpos * inclusive matrix inverse  
            wPnt = pN[0]*iIMatrix 
            #fnCurve.setCVPosition(idx, wPnt)
            
            #print fnCurve.getParamAtPoint(pN[0]*iIMatrix, 1000)
            pass
        else:
            wPnt = i
        cvs.append(wPnt)
    fnCurve.setCVPositions(cvs)
    fnCurve.updateCurve()
    iterSelList.next()
    
print time.clock() - tick
