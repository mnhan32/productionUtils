#

def abcImporter():
    defaultPath=cmds.workspace(q=True,dir=True)
    f=cmds.fileDialog2(cap="Import Alembic Files",fileFilter="Alembic Files(*.abc)",dir=defaultPath,dialogStyle=2,fm=4,okc="Import")
    if f:
        if not cmds.pluginInfo("AbcImport", query=True, l=True):
            cmds.loadPlugin("AbcImport")
        for i in f:
            mel.eval('AbcImport -mode import "%s"'%i)

def abcExporter():
    import os
    defaultPath=cmds.workspace(q=True,dir=True)
    publishEle = os.path.abspath(os.path.join(defaultPath, '../../publish/elements'))
    print defaultPath, publishEle
    if os.path.isdir(publishEle):
        defaultPath = publishEle
    else:
        print 'no'
    f=cmds.fileDialog2(cap="Export Alembic Files",fileFilter="Alembic Files(*.abc)",dir=defaultPath,dialogStyle=2,fm=4,okc="Export")
    print f
    #cmds.AbcExport(j="-frameRange 1 1 -noNormals -worldSpace -dataFormat ogawa -root fat -file T:/Han/test11.abc")
