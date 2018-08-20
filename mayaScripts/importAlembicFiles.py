import maya.cmds as cmds
import maya.mel as mel

defaultPath=cmds.workspace(q=True,dir=True)
f=cmds.fileDialog2(cap="Import Alembic Files",fileFilter="Alembic Files(*.abc)",dir=defaultPath,dialogStyle=2,fm=4,okc="Import")
if f:
    if not cmds.pluginInfo("AbcImport", query=True, l=True):
        #pPath=cmds.pluginInfo("AbcImport",q=True,p=True)
        #print pPath
        cmds.loadPlugin("AbcImport")
    for i in f:
        mel.eval('AbcImport -mode import "%s"'%i)
