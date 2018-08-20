import maya.api.OpenMaya as om
import maya.cmds as cmds
import time

def removeCurveWithinRadius(r=0.25, d=False, re=True):
    if d:
        tick = time.clock()
    radius = r
    sel = om.MGlobal.getActiveSelectionList()
    delCurve = om.MDagPathArray()

    for s in range(sel.length()):    
        sourcePath = sel.getDagPath(s)
        count = s + 1      
        if not sourcePath in delCurve:           
            sMatrix = sourcePath.inclusiveMatrix()
            sourceFnCurve = om.MFnNurbsCurve(sourcePath)
            sourceCVPos =  sourceFnCurve.cvPosition(0) * sMatrix
                    
            for c in range(count, sel.length()):            
                tarPath = sel.getDagPath(c)
                print sourcePath.fullPathName()
                print tarPath.fullPathName()
                if not tarPath in delCurve:
                    tMatrix = tarPath.inclusiveMatrix()
                    tarFnCurve = om.MFnNurbsCurve(tarPath)
                    tarCVPos = tarFnCurve.cvPosition(0) * sMatrix
                    
                    if abs(tarCVPos.x - sourceCVPos.x) <= radius and abs(tarCVPos.y - sourceCVPos.y) <= radius and abs(tarCVPos.z - sourceCVPos.z) <= radius:
                        dist = sourceCVPos.distanceTo(tarCVPos)
                        print dist
                        if dist <= radius:
                            delCurve.append(tarPath)           

    if d:
        print 'total run time ', time.clock()-tick
    
    if not d:    
        cmds.delete([i.fullPathName() for i in delCurve])
    else:
        cmds.select([i.fullPathName() for i in delCurve], r=True)
    
    if re:
        return [i for i in sel if i not in delCurve];
    else:
        return delCurve;
    
