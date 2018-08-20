import maya.cmds as cmds
import maya.mel as mel
import os, shutil

sel = cmds.ls(sl=True)
if not sel:
    cmds.error( 'You must select a yeti node')

dF = cmds.fileDialog2(ds=1, fm=3)
if dF:
    newpath = dF[0]
    tex = mel.eval('pgYetiGraph -listNodes -type "texture" %s'%sel[0])
    for t in tex:
        fName = mel.eval('pgYetiGraph -node %s -param "file_name" -getParamValue %s'%(t, sel[0]))
        targetPath = os.path.join(newpath, os.path.basename(fName)).replace('\\','/')
        shutil.copy(fName, targetPath)
        mel.eval('pgYetiGraph -node %s -param "file_name" -setParamValueString %s %s'%(t,targetPath,sel[0]))
