import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel
import time


mayaVersion = cmds.about(v=True)
if '2017' in mayaVersion:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
elif '2016' in mayaVersion:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from shiboken import wrapInstance

def doIt():
    global mainWin
    try:
        mainWin.close()
    except: pass
    mainWin = RebuildGroomWindows(maya_main_window())
    mainWin.show()

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)
    

class RebuildGroomWindows(QMainWindow):
    def __init__(self, parent=None):
        super(RebuildGroomWindows, self).__init__(parent)
        self.scriptVersion = '0.1'
        self.__buildUi()
    
    def __buildUi(self):
        vlay = QVBoxLayout(self)
        
        

def removeCurveWithinRadius(r=0.5, d=False):
    if d:
        tick = time.clock()
    radius = r
    sel = om.MGlobal.getActiveSelectionList()
    delCurve = om.MDagPathArray()
    print '[ Info ] : Processing Remove Double .......'
    for s in range(sel.length()):    
        sourcePath = sel.getDagPath(s)
        count = s + 1
        sName = sourcePath.fullPathName()
        
        if not sourcePath in delCurve:
                       
            sMatrix = sourcePath.inclusiveMatrix()
            sourceFnCurve = om.MFnNurbsCurve(sourcePath)
            sourceCVPos =  sourceFnCurve.cvPosition(0) * sMatrix
                    
            for c in range(count, sel.length()):            
                tarPath = sel.getDagPath(c)

                if not tarPath in delCurve:
                    tMatrix = tarPath.inclusiveMatrix()
                    tarFnCurve = om.MFnNurbsCurve(tarPath)
                    tarCVPos = tarFnCurve.cvPosition(0) * sMatrix
                    
                    if abs(tarCVPos.x - sourceCVPos.x) <= radius and abs(tarCVPos.y - sourceCVPos.y) <= radius and abs(tarCVPos.z - sourceCVPos.z) <= radius:
                        dist = sourceCVPos.distanceTo(tarCVPos)
                        #print dist
                        if dist <= radius:
                            delCurve.append(tarPath)
                            
      

    if d:
        print 'total run time ', time.clock()-tick  
          
    print '[ Info ] : Finishing Remove Double .......'
    return [i.fullPathName() for i in delCurve]

def rebuildGroom(removeDouble=True, radius=0.025, avoidInside=False, maxDist=10.0, alongNormal=0.02 ):
    
    
    
    tick = time.clock()
    newGroom = 'pgYetiGroom'#this is hard coded name, caz Yeti won't return new groom name
    groom = cmds.ls(sl=True)
    step = 0.2
       
    if groom:
        for g in groom:
            gShape = cmds.listRelatives(g, s=True, f=True, type='pgYetiGroom')
            if gShape:
                pGroup = cmds.listRelatives(g, p=True)
                inputMesh = cmds.listConnections('%s.inputGeometry'%gShape[0], sh=True, s=True, d=False)
                yetiPrim = cmds.listConnections('%s.outputData'%gShape[0], sh=True, s=False, d=True )
                
                groomName = g.split('|')[-1]                
                print '[ Info ] : Processing Rebuild Groom %s .......'%groomName    
                    
                if inputMesh:
                    iMesh = inputMesh[0]
                    targetMesh =  cmds.listRelatives(iMesh, p=True)[0]
                    cmds.select(g, r=True)
                    mel.eval('pgYetiConvertGroomToCurves;')                   
                    outputCurves = cmds.ls('%s_strand_*'%gShape[0].split('|')[-1], type='transform', l=True) 
                    
                    
                    #for curve post process if necessary
                    #
                    
                    if removeDouble:
                        try:
                            cmds.select(outputCurves, r=True)
                            doubleCurves = removeCurveWithinRadius(r=radius)
                            cmds.delete(doubleCurves)
                            outputCurves = [i for i in outputCurves if i not in doubleCurves]
                        except:
                            print 'failed to remove double curves within radiud.'
                    
                    if avoidInside:
                        
                        print '[ Info ] : Processing NurbsCurveEPToClosestPointOnMesh .......'
                        
                        cmds.select(outputCurves.append(tarMesh), r=True)
                        try:
                            cmds.loadPlugin( 'NurbsCurveEPToClosestPointOnMesh' )
                        except:
                            print "NurbsCurveEPToClosestPointOnMesh plugin not existed, or failed."
                        try:
                            mel.eval("NurbsCurveEPToClosestPointOnMesh -a %f -m %f;"%(alongNormal, maxDist))
                        except:
                            print 'failed to move nurbs curve endpoints to closest points on mesh.'
                            
                        print '[ Info ] : Finishing NurbsCurveEPToClosestPointOnMesh .......'
                        
                    #
                    #end of curve post process
                    
                    setName = cmds.sets(outputCurves, n='%s_set'%gShape[0].split('|')[-1])

                    mel.eval('pgYetiConvertGuideSetToGroom("%s", "%s", %f);'%(setName, iMesh, step))
                    cmds.delete(outputCurves)
                    
                    cmds.delete(g)
                    cmds.rename(newGroom, groomName)
                    
                    if pGroup:      
                        cmds.parent(groomName, pGroup)
                    
                    if yetiPrim:
                        yetiP = yetiPrim[0]           
                        mel.eval('pgYetiAddGroom("%s", "%s");'%(gShape[0],yetiP))
                        
                    print '[ Info ] : Finishing Rebuild Groom %s .......'%groomName
                    
                   
    #cmds.select(cl=True)                
    print '[ Info ] : Job finished in %f sec.'%(time.clock()-tick)


#rebuildGroom(removeDouble=True, radius=0.5)
rebuildGroom(removeDouble=False, radius=0.5)
rebuildGroom(removeDouble=False, radius=0.5, avoidInside=False, maxDist=10.0, alongNormal=0.02)
