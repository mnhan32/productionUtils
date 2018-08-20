import maya.cmds as cmds
import random,math
sel=cmds.ls(sl=True,l=True)
#start frame
start=840
#end frame - 1
end=1200

#freq
speedW=1

#XYZ multiplier
mulX=1
mulY=.5    
mulZ=1


for i in range(start,end):
    for x in sel:
        cmds.currentTime(i)
        rot=cmds.keyframe(x,q=True,vc=True,index=(0,),at='rotate')
 
        if i==start:        
            cmds.setKeyframe(x,at='rotate')
        else:
            rot[0]=rot[0]+(random.uniform(-1,1)*math.sin(random.randint(0,800)+cmds.currentTime(q=True)*speedW)*mulX)
            rot[1]=rot[1]+(random.uniform(-1,1)*math.sin(random.randint(0,800)+cmds.currentTime(q=True)*speedW)*mulY)
            rot[2]=rot[2]+(random.uniform(-1,1)*math.sin(random.randint(0,800)+cmds.currentTime(q=True)*speedW)*mulZ)
            
            cmds.setKeyframe(x,v=rot[0],at='rotateX')
            cmds.setKeyframe(x,v=rot[1],at='rotateY')
            cmds.setKeyframe(x,v=rot[2],at='rotateZ')
              
