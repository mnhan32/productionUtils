#Import api modules
import maya.OpenMaya as api
import maya.OpenMayaUI as apiUI
import maya.cmds as cmds
import os

#get Scene name
sName=cmds.file(q=True,sn=True)
if sName:
    sName='_'.join(os.path.basename(sName).split('.')[0:-1])

else:
    sName='Untitled'
    
#Grab the last active 3d viewport
view = apiUI.M3dView.active3dView()
img = api.MImage()
cam = api.MDagPath()

#get view camera name
view.getCamera(cam)
camName=''.join(cam.partialPathName().split('|'))
#camName=cam.fullPathName()


if view.getRendererName() == view.kViewport2Renderer:      
    img.create(view.portWidth(), view.portHeight(), 4, api.MImage.kFloat)
    view.readColorBuffer(img)
    img.convertPixelFormat(api.MImage.kByte)
else:
    view.readColorBuffer(img)

#read the color buffer from the view, and save the MImage to disk
fName='%s_%s'%(sName,camName)
img.writeToFile('D:/%s.jpg'%fName, 'jpg')
