import maya.cmds as cmds
sel=cmds.ls(sl=True,l=True)
cFrame=cmds.currentTime(q=True)
for i in sel:
    loc=cmds.spaceLocator(n='Ref_loc')
    cmds.parentConstraint(i,loc,mo=False)
    try:
        cmds.addAttr(loc[0],ln='speedKM',at='float',h=False,k=True)
    except:
        pass
    cmds.expression(o=loc[0],s="float $cTime=`currentTime -q`;\nfloat $cPos[];\n$cPos[0]="+loc[0]+".translateX;\n$cPos[1]="+loc[0]+".translateY;\n$cPos[2]="+loc[0]+".translateZ;\nfloat $pPos[]=eval(\"getAttr -t \"+string($cTime-1) +\" \\\""+loc[0]+".translate\\\"\");\nfloat $dist=sqrt(($cPos[0]-$pPos[0])*($cPos[0]-$pPos[0])+($cPos[1]-$pPos[1])*($cPos[1]-$pPos[1])+($cPos[2]-$pPos[2])*($cPos[2]-$pPos[2]));\n"+loc[0]+".speedKM=$dist*24*60*60/100/1000;");
