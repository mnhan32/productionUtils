#######################################################
# by Menghan Ho
# 2017/03/28
# this script export active clip lens info as a txt file to the same dir where blende file located
#
import bpy
import os

fpath = bpy.data.filepath
fDir = os.path.dirname(fpath)
fName = os.path.basename(fpath).split('.')[0:-1][0]
outName = os.path.join(fDir,'%s_LensInfo.txt'%fName)
print('export lens info to %s'%outName)
for area in bpy.context.screen.areas:
    if area.type == 'CLIP_EDITOR':
        sw = area.spaces[0].clip.tracking.camera.sensor_width
        fl = area.spaces[0].clip.tracking.camera.focal_length
        cx= area.spaces[0].clip.tracking.camera.principal[0]
        cy= area.spaces[0].clip.tracking.camera.principal[1]
        model = area.spaces[0].clip.tracking.camera.distortion_model
        k1 = area.spaces[0].clip.tracking.camera.k1
        k2 = area.spaces[0].clip.tracking.camera.k2
        k3 = area.spaces[0].clip.tracking.camera.k3       
        dataOut = 'sensor width:%s\nfocal length:%s\ncx:%s\ncy:%s\nmodel:%s\nk1:%s\nk2:%s\nk3:%s'%(sw,fl,cx,cy,model,k1,k2,k3)
        print(dataOut)
        with open(outName, 'w+') as out:
            out.write(dataOut)
        
