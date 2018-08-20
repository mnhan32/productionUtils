from __future__ import print_function

from PySide import QtGui,QtCore
from shiboken import wrapInstance
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui

from ui_DeformerOnMesh import ui_DeformerOnMesh as baseUI
reload(baseUI)


# Run following in Maya python, if you have PYTHONPATH point to defomerOnMesh parent folder
'''
from deformerOnMesh import deformerOnMesh as dOM
reload(dOM)
dOM.doIt()
'''

def getUVFromPosition(inMesh, pPos):
    selectionList = om.MSelectionList()
    selectionList.add(inMesh)
    dagPath = om.MDagPath()
    selectionList.getDagPath(0, dagPath)
    fnMesh = om.MFnMesh(dagPath)
    fnMesh = om.MFnMesh(dagPath)
    x1 = om.MScriptUtil()
    x1.createFromList( [0.0,0.0], 2 )
    uvPoint = x1.asFloat2Ptr()    
    fnMesh.getUVAtPoint(om.MPoint(pPos[0],pPos[1],pPos[2]),uvPoint,om.MSpace.kWorld)        
    uVal=om.MScriptUtil.getFloat2ArrayItem(uvPoint, 0, 0)
    vVal=om.MScriptUtil.getFloat2ArrayItem(uvPoint, 0, 1)   
     
    return [uVal,vVal]
    
def doIt():
    global mainWin
    try:
        mainWin.close()
    except: pass
    mainWin = deformerOnMesh(maya_main_window())
    mainWin.show()

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtGui.QWidget)

class deformerOnMesh(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super( deformerOnMesh, self).__init__(parent)
        self.ui =baseUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()
        
        
    def init(self):
        self.__oriTransform=''    
        self.__oriMesh = ''
        self.__tarMesh = ''
        self.__baseVertex = ''
        self.__sMod = ''
        self.__sModHandle = ''
        self.__follicle = ''
        self.__follicleShape = ''

        self.__softRatio = 20.0
        self.__cluseterRange = 3
        self.__newbuild = False
        self.forceNewBuild = False
        self.useSetting = False

        self.__prefixName = 'dOM_Mesh'
        self.__prefixObjName = 'dOM_Obj'

        self.__listenerId=[]

        self.__setupUIElement()

    def __setupUIElement(self):
        self.ui.btn_run.clicked.connect(self.__build)        
        self.ui.cB_forceNew.clicked.connect(lambda:self.__checkBoxStateChange(self,self.ui.cB_forceNew,'forceNewBuild'))
        self.ui.gB_setting.clicked.connect(lambda:self.__checkBoxStateChange(self,self.ui.gB_setting,'useSetting'))
        
    '''
    def closeEvent( self, event ):
        for k in self.__listenerId:
            cmds.scriptJob( kill=k, force=True ) 
        super( deformerOnMesh, self ).closeEvent( event ) 
    '''

    def __checkBoxStateChange(self,*arg):
        if arg[1].isChecked():
            setattr(self,arg[2],True)
        else:
            setattr(self,arg[2],False)
        self.__outputMsg('Checkbox', '%s set to %s'%(arg[2], getattr(self,arg[2])))
    

    def __build(self):        
        result = self.__buildValidation()
        if result[0] == 0 :
            for k in result[1]:
                self.__outputMsg('Build', 'Building %s'%k,None)
                inData = k.split('.')
                
                #check selection, get base shape node and transform node
                if cmds.objectType(inData[0]) == 'transform':
                    parentT = inData[0]
                    inData[0] = cmds.listRelatives(inData[0],s=True,ni=True)[0]
                else:
                    parentT = cmds.listRelatives(inData[0], p=True, type='transform')[0]
                
                self.__oriMesh = inData[0]
                self.__baseVertex = inData[1]
                self.__oriTransform = parentT
                #generate build
                if self.forceNewBuild:
                    self.__createNewBuild()
                    self.__newbuild = True
                else:
                    if cmds.attributeQuery(self.__prefixName, node=self.__oriMesh, ex=True):
                        self.__tarMesh = cmds.getAttr('%s.%s'%(self.__oriMesh,self.__prefixName))
                        self._newbuild = False
                        if not cmds.objExists(self.__tarMesh):
                            self.__outputMsg('Err', '%s is not valid, check its attrbute from %s.'%(self.__tarMesh,self.__oriMesh),'err') 
                    else:
                        self.__createNewBuild()
                        self.__newbuild = True                        
                        self.__outputMsg('Msg', 'There is no existed build, this is a new build.') 
                
                self.__generateFollicleAndDeformer()
                
    def __createNewBuild(self):
        tmpDup = cmds.duplicate(self.__oriTransform, ic=False)[0]
        tmpMesh = cmds.listRelatives(tmpDup,s=True,ni=True)[0]
        tmpName = self.__oriMesh
        self.__oriMesh = cmds.rename(self.__oriMesh, '%s_Hold'%self.__oriMesh)

        self.__tarMesh =  cmds.createNode('mesh',parent=self.__oriTransform, n='%s_MESH'%self.__prefixName)
        cmds.setAttr('%s.visibility'%self.__tarMesh, 0)
        cmds.setAttr('%s.intermediateObject'%self.__tarMesh, 1)
        cmds.connectAttr('%s.outMesh'%self.__oriMesh, '%s.inMesh'%self.__tarMesh)
        
        cmds.refresh()
        
        cmds.parent(tmpMesh,self.__oriTransform, s=True,r=True)
        tmpMesh = cmds.rename(tmpMesh, tmpName)
        
        cmds.delete(tmpDup)
        cmds.setAttr('%s.visibility'%self.__oriMesh, 0)
        cmds.setAttr('%s.intermediateObject'%self.__oriMesh, 1) 
        cmds.connectAttr('%s.outMesh'%self.__oriMesh, '%s.inMesh'%tmpMesh)         

        self.__oriMesh = tmpMesh


    def __generateFollicleAndDeformer(self):
        #get uv from point position
        pPos = cmds.pointPosition( self.__tarMesh + '.' + self.__baseVertex, w=True)
        uv = getUVFromPosition(self.__oriMesh, pPos)

        
        cmds.select(self.__oriMesh + '.' + self.__baseVertex, r=True)

        if self.useSetting :
            self.__cluseterRange  = self.ui.sB_growth.value()
            self.__softRatio = self.ui.dSB_falloff.value()
            print('usr setting')

        
        for i in range(self.__cluseterRange):
            cmds.GrowPolygonSelectionRegion()
        
        
        bbox = cmds.polyEvaluate(bc=True)
        allSize = [(bbox[0][1]-bbox[0][0]), (bbox[1][1]-bbox[1][0]), (bbox[2][1]-bbox[2][0])]        
        fallOffRatio = sorted(allSize)[-1]*((100 - self.__softRatio)*.01)

        sMod = cmds.softMod(rel=True, dt=True, fas=False, fc=pPos, fr=fallOffRatio, fm=False, fom=0)
        
        self.__sMod = sMod[0]
        self.__sModHandle = sMod[1]
        sModHandleShape = cmds.listRelatives(sMod[1],s=True,ni=True,f=True)[0]

        #add attribute to store tarMesh, this is necessary 
        #because generate softMod on a new build will create a different Shape node
        if self.__newbuild:
            newShape = cmds.listRelatives(self.__oriTransform,s=True,ni=True)[0]
            if not cmds.attributeQuery(self.__prefixName, node=newShape, ex=True):
                cmds.addAttr(newShape,ln=self.__prefixName,dataType='string')
            cmds.setAttr('%s.%s'%(newShape,self.__prefixName), l=False)
            cmds.setAttr('%s.%s'%(newShape,self.__prefixName), self.__tarMesh, type='string')
            cmds.setAttr('%s.%s'%(newShape,self.__prefixName), l=True)

        #creating follicle and add softMod
        fol = cmds.createNode('follicle')
        folT = cmds.listRelatives(p=True)[0]

        self.__follicle = folT
        self.__follicleShape = fol
        cmds.connectAttr('%s.outTranslate'%fol,'%s.translate'%folT)
        cmds.connectAttr('%s.outRotate'%fol,'%s.rotate'%folT)
        cmds.connectAttr('%s.worldMatrix[0]'%self.__tarMesh,'%s.inputWorldMatrix'%folT)
        cmds.connectAttr('%s.outMesh'%self.__tarMesh,'%s.inputMesh'%folT)
        cmds.setAttr('%s.simulationMethod'%folT,0)
        cmds.setAttr('%s.parameterU'%folT,uv[0])
        cmds.setAttr('%s.parameterV'%folT,uv[1])        
        
        

        #add tag to all created obj   
        cmds.addAttr(self.__sMod,ln=self.__prefixObjName,dataType='string')
        cmds.setAttr('%s.%s'%(self.__sMod,self.__prefixObjName), 'SOFTMOD', type='string')
        cmds.setAttr('%s.%s'%(self.__sMod,self.__prefixObjName), l=True)
        cmds.addAttr(self.__follicle,ln=self.__prefixObjName,dataType='string')
        cmds.setAttr('%s.%s'%(self.__follicle,self.__prefixObjName), 'FOLLICLE_TRANSFORM', type='string')
        cmds.setAttr('%s.%s'%(self.__follicle,self.__prefixObjName), l=True)
        cmds.addAttr(self.__follicleShape,ln=self.__prefixObjName,dataType='string')
        cmds.setAttr('%s.%s'%(self.__follicleShape,self.__prefixObjName), 'FOLLICLE', type='string')
        cmds.setAttr('%s.%s'%(self.__follicleShape,self.__prefixObjName), l=True)
        cmds.addAttr(self.__sModHandle,ln=self.__prefixObjName,dataType='string')
        cmds.setAttr('%s.%s'%(self.__sModHandle,self.__prefixObjName), 'HANDLE TRANSFORM', type='string')
        cmds.setAttr('%s.%s'%(self.__sModHandle,self.__prefixObjName), l=True)
        cmds.addAttr(sModHandleShape,ln=self.__prefixObjName,dataType='string')
        cmds.setAttr('%s.%s'%(sModHandleShape,self.__prefixObjName), 'HANDLE', type='string')
        cmds.setAttr('%s.%s'%(sModHandleShape,self.__prefixObjName), l=True)
        
        tGrp = cmds.group(em=True, n='grp_%s'%sMod[1])    
        cmds.parent(sMod[1], tGrp)        
        #cmds.parent( tGrp, folT)
        cmds.parentConstraint(folT, tGrp, mo=True)
        cmds.connectAttr('%s.center'%folT,'%s.falloffCenter'%sMod[0])
        cmds.connectAttr('%s.parentInverseMatrix[0]'%sMod[1], '%s.bindPreMatrix'%sMod[0])
        
        #add tag to group
        cmds.addAttr(tGrp,ln=self.__prefixObjName,dataType='string')
        cmds.setAttr('%s.%s'%(tGrp,self.__prefixObjName), 'GROUP', type='string')
        cmds.setAttr('%s.%s'%(tGrp,self.__prefixObjName), l=True)

        #done building graph, select soft modification node for user
        cmds.select(self.__sModHandle,r=True)
    '''
    def __removeAllDeformers(self):
        tarMesh = self.__returnTarMesh()
        if tarMesh[0] == 0:
            handle=[]
            for i in tarMesh[1]:
                result = self.__toHandle(i)
                if result:
                    handle.append(result)
            if handle:
                pass
        else:
            self.__outputMsg('Invalid','No valid mesh in selection','warn')


            
    
    def __resetAllDeformers(self):
        pass
    
    def __editMemberSet(self):
        pass
    
    def __toHandle(self, tarMesh):
        follicle = cmds.listConnections('%s.outMesh'%tarMesh, d=True)
        if follicle:
            return follicle[0]
        else:
            return None
            self.__outputMsg('Missing', 'Can not find linked follicle', 'warn')
        
    
    def __toAllHandle(self):
        pass

    def __returnTarMesh(self):
        sel = cmds.ls(sl=True,l=True)
        processSel = []
        for k in sel:
            sNode = cmds.listRelatives(k, s=True, ni=True, f=True, type='mesh')
            if sNode:
                if self.__validateCustomObj(sNode[0])[0] == 0:
                    processSel.append(k)
        
        if processSel:
            return [0, processSel]
        else:
            return [1]
    '''
    def __validateCustomObj(self, inputObj):
        if cmds.attributeQuery(self.__prefixObjName, node=inputObj, ex=True):
            return 0           
        else:
            return 1

    def __validateDeoformerOnMesh(self, inputMesh):
        if cmds.attributeQuery(self.__prefixName, node=inputMesh, ex=True):
            tarMesh = cmds.getAttr('%s.%s'%(inputMesh,self.__prefixName))
            if cmds.objExists(tarMesh):
                return [0, tarMesh]
            else:
                self.__outMsg('Invalid','found attr, but obj not existed.', 'err')
                return [1]
        else:
            self.__outMsg('Invalid','This is not a valid mesh.', 'err')
            return [1]

    def __buildValidation(self):
        selVertex = cmds.ls(sl=True, l=True, fl=True)  
        
        validSel = []
        for k in selVertex:                        
            splitSel = k.split('.')
            if 'vtx' in splitSel[-1]:                
                validSel.append(k) 
                
        if validSel:
            if not (len(validSel) == len(selVertex)):
                self.__outputMsg('Remove Invalid Selection','At least one selection is invalid','warn')
        else:
            self.__outputMsg('No Valid Selection','Either selection is empty or you need to select at least one vertex','err')
            return [1]
            
        return [0,validSel]
        
    def __outputMsg(self, msgCat, msg, msgType=None):
        msgTxt = '%s : %s'%(msgCat, msg)
        if msgType:
            msgType.upper()
        else:
            msgType = 'Msg'
            
        statusBarTxt = '%s : %s'%(msgType, msg)
        self.ui.statusbar.showMessage (statusBarTxt, 3000)        
        if msgType == 'err':
            cmds.error(msgTxt)
        elif msgType == 'warn':
            cmds.warning(msgTxt)
        elif msgType == None:
            print(msgTxt)
        
            
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = deformerOnMesh()
    ret = app.exec_()
    sys.exit(ret)
