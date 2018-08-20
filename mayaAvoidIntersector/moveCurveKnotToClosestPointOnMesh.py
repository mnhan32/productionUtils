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

'''
tickIntersector = time.clock()
intersector = om.MMeshIntersector()
intersector.create(mesh.node())
print 'intersector',time.clock()-tickIntersector
'''

while not iterSelList.isDone():
    curvePath = iterSelList.getDagPath()    
    iMatrix = curvePath.inclusiveMatrix()
    iIMatrix = curvePath.inclusiveMatrixInverse()
    fnCurve = om.MFnNurbsCurve(iterSelList.getDependNode())
    curveNode = curvePath.node()
    knts = fnCurve.knots()
    deg = fnCurve.degree
    #knts = knts[2:-2]
    count = 0
    eps = om.MPointArray()
    for idx, i in enumerate(knts):
        tickQueryPnt = time.clock()
        #object space to worldspace, worldpos = localpos * inclusive matrix      
        wPnt = fnCurve.getPointAtParam(i)*iMatrix
        print 'per pnt query time',time.clock()-tickQueryPnt
        #print wPnt
        #tickIntersectorCal = time.clock()
        #mPnt = intersector.getClosestPoint(wPnt, 5)
        #print 'cal intersector', time.clock()-tickIntersectorCal
        #print mPnt.point
        #print mPnt.normal
        
        tickGetClosest = time.clock()
        pN = fnMesh.getClosestPointAndNormal(wPnt, space=om.MSpace.kWorld) 
        print 'cal get closest pnt data ',time.clock()-tickGetClosest
        
        tickCalInside = time.clock()        
        vecToPnt = wPnt-pN[0]
        vecToPnt.normalize()        
        dotP = vecToPnt*pN[1]#if dot product < 0, point is inside of mesh      
        print 'cal find inside ',time.clock()-tickCalInside
        
        tickProcessPntData = time.clock() 
        if dotP < 0:
            wPnt = pN[0]
            count += 1  
            if idx > 2:
                wPnt += 0.1*pN[1]               
            
        eps.append(wPnt)
        print 'cal process pnt data ',time.clock()-tickProcessPntData 
        
    if count>0:        
        tickBuild = time.clock()
        om.MFnNurbsCurve().createWithEditPoints(eps,fnCurve.degree,fnCurve.form, 0,1,0)	
        print 'build curve time',time.clock()-tickBuild
    iterSelList.next()
print 'total run time ', time.clock()-tick
