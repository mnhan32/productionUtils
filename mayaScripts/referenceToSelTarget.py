import maya.cmds as cmds
refF='X:/MMJ/assets/Prop/Orange_Tree/rig/publish/maya/leaf.ma'
sel=cmds.ls(sl=True,l=True)
for i in sel:
    trans=cmds.xform(i,q=True,ws=True,t=True)
    rot=cmds.xform(i,q=True,ws=True,ro=True)
    sca=cmds.xform(i,q=True,ws=True,s=True)
    
    
    fName=cmds.file(refF,r=True,type="mayaAscii",ignoreVersion=True,gl=True,mergeNamespacesOnClash=False,namespace="leaf",options="v=0;")
    rfn=cmds.referenceQuery(fName,rfn=True)
    tar='%s:root_ctrl'%cmds.referenceQuery(rfn,ns=True)
    #print tar
    cmds.xform(tar,ws=True,t=(trans[0],trans[1],trans[2]))
    cmds.xform(tar,ws=True,ro=(rot[0],rot[1],rot[2]))
    cmds.xform(tar,ws=True,s=(sca[0],sca[1],sca[2]))
