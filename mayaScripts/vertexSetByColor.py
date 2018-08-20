'''
vertexSetByColor
split geo verext into two selection sets based on vertex color( red channel) 
Usage : select geo transform, not mesh
        set threshold
        run def
'''


import maya.cmds as cmds

def vertexSetByColor(geo, threshold):
    count = cmds.polyEvaluate(geo,vertex=True)
    colorAtR = cmds.polyColorPerVertex('%s.vtx[0:]'%geo, query=True, r=True)
    selInside = []
    selOutside = []
    for i in range(count):
        if colorAtR[i] > threshold:
            selInside.append('%s.vtx[%i]'%(geo, i))
        else:
            selOutside.append('%s.vtx[%i]'%(geo, i))
        
    cmds.sets(selInside, n="polyInside")
    cmds.sets(selOutside, n="polyOutside")


#sel = cmds.ls(sl=True, fl=True)
#threshold=0.5
#vertexSetByColor(sel[0], threshold)
    
