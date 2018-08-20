import maya.cmds as cmds
import re, os

sel = cmds.ls(sl=True,l=True)


#chan file source
multipleFilters = "Chan Files (*.chan)"
chanFile = cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=1, fileMode=1)

if chanFile[0]:
    chanBaseName = '_'.join( os.path.basename(chanFile[0]).split('.')[0:-1] )
    locTime = cmds.createNode('time')
    locTime = cmds.rename(locTime, 'chainImport')
    f = open(chanFile[0], 'r')
    
    #reformat chan data into array
    data=[]
    sw = 1
    for idx, line in enumerate(f):
        cleanData = re.sub("\r\n", "", line)
        splitData = cleanData.split('\t')
        if len(splitData)==1:
            if sw:
                sw = 0
                cmds.warning('Chan file only contain 1 col, will use current frame as starting frame.')            
                cFrame = cmds.currentTime(q=True)
            splitData = [cFrame + idx] + splitData
        data.append(splitData[0:2])
    
    f.close()
    #read array
    for i in data:
        #subject to change how to map value
        #round
        i = [round(float(k)) for k in i]
        #print 'Frame : %s , tx: %s, ty: %s, tz: %s, rx: %s, ry: %s, rz: %s'%(i[0],i[1],i[2],i[3],i[4],i[5],i[6])   
        cmds.setKeyframe( locTime, at='o', time=(i[0],i[0]), v=i[1])
     
    
    #connect 
    inW=cmds.listConnections('%s.o'%locTime,s=True, d=False)[0]
    #print inW, chanBaseName
    nName = cmds.rename(inW, chanBaseName)
    cmds.connectAttr('%s.apply'%nName, 'time1.timewarpIn_Raw', f=True)
    cmds.delete(locTime)
