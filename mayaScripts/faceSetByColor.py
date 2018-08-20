'''
faceSetByColor
split geo face into two selection sets based on vertex color( red channel) 

'''

import maya.cmds as cmds

def faceSetByColor(geo, threshold):
    count = cmds.polyEvaluate(geo,vertex=True)
    faceCount = cmds.polyEvaluate(f=True)
    colorAtR = cmds.polyColorPerVertex('%s.vtx[0:]'%geo, query=True, r=True)
    
    selInside = []
    selOutside = []
    for f in range(faceCount):
        vtxList = [ i.encode('ascii','ignore') for i in cmds.polyInfo('%s.f[%s]'%(geo, f), fv=True)[0].split(':')[1].split(' ') if i.encode('ascii','ignore').isdigit()]
        switch = 1
        for v in vtxList:   
            if colorAtR[int(v)] > threshold:
                selInside.append('%s.f[%s]'%(geo, f))
                switch = 0
                break
        if switch :
            selOutside.append('%s.f[%s]'%(geo, f))

    cmds.sets(selInside, n="polyInside")
    cmds.sets(selOutside, n="polyOutside") 


sel = cmds.ls(sl=True, fl=True)
threshold=0.5
faceSetByColor(sel[0], threshold)
