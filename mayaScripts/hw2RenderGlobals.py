import maya.cmds as cmds
import maya.mel as mel


fileImagePrefix = '<Scene>'
sFrame=1001
eFrame=1020

cmds.setAttr('defaultRenderGlobals.ren', 'mayaHardware2', type='string')
mel.eval('unifiedRenderGlobalsRevertToDefault;')#set render global to default first

#Render Globals
#Color Management
mel.eval("colorManagementPrefs -e -ote 1;")
tarOutTransform = 'Rec 709 gamma'
#avaialableOutTransform = mel.eval("colorManagementPrefs -q -ots")
try:
    mel.eval('colorManagementPrefs -e -otn "%s";'%tarOutTransform)
except:
    loadedOutTransform = mel.eval('colorManagementPrefs -q -otn;')
    print '%s not found, use default %s instead.'%(tarOutTransform, loadedOutTransform)

#File Output
cmds.setAttr('defaultRenderGlobals.imageFilePrefix', fileImagePrefix, type='string')
cmds.setAttr('defaultRenderGlobals.imageFormat', 32)# 8:jpg, 32:png, 3:tiff, 4:tiff16, 40:exr
cmds.setAttr('defaultRenderGlobals.imageFilePrefix', fileImagePrefix, type='string')
#frame/animation ext
cmds.setAttr('defaultRenderGlobals.outFormatControl', 0)
cmds.setAttr('defaultRenderGlobals.animation', 1)
cmds.setAttr('defaultRenderGlobals.putFrameBeforeExt', 1)
cmds.setAttr('defaultRenderGlobals.periodInExt', 1)
#frame padding
cmds.setAttr('defaultRenderGlobals.extensionPadding',4)

#frame range
cmds.setAttr('defaultRenderGlobals.startFrame', sFrame)
cmds.setAttr('defaultRenderGlobals.endFrame', sFrame)
cmds.setAttr('defaultRenderGlobals.byFrameStep', 1)

#skip existed, and renumber
'''
cmds.setAttr('defaultRenderGlobals.skipExistingFrames', 0)
cmds.setAttr('defaultRenderGlobals.modifyExtension', 0)
cmds.setAttr('defaultRenderGlobals.startExtension', 1)
cmds.setAttr('defaultRenderGlobals.byExtension', 1)
'''

#Hardware Render
#Performance
cmds.setAttr('hardwareRenderingGlobals.consolidateWorld',0)

setAttr "hardwareRenderingGlobals.vertexAnimationCache" 0;
setAttr "hardwareRenderingGlobals.maxHardwareLights" 8;
setAttr "hardwareRenderingGlobals.transparencyAlgorithm" 1;

#Texure Resolition Clamping
setAttr "hardwareRenderingGlobals.enableTextureMaxRes" 0;
setAttr "hardwareRenderingGlobals.textureMaxResolution" 4096;

#AO
cmds.setAttr('hardwareRenderingGlobals.ssaoEnable', 1)
cmds.setAttr('hardwareRenderingGlobals.ssaoAmount', 1)
cmds.setAttr('hardwareRenderingGlobals.ssaoRadius', 16)
cmds.setAttr('hardwareRenderingGlobals.ssaoFilterRadius',16)
cmds.setAttr('hardwareRenderingGlobals.ssaoSamples', 16)

#Hardware Fog
setAttr "hardwareRenderingGlobals.hwFogFalloff" 0;
setAttr "hardwareRenderingGlobals.hwFogDensity" .2;#only in non linear
setAttr "hardwareRenderingGlobals.hwFogStart" 0;#linear 0
setAttr "hardwareRenderingGlobals.hwFogEnd" 100;#linear 0
setAttr "hardwareRenderingGlobals.hwFogAlpha" 1;
setAttr "hardwareRenderingGlobals.hwFogColor" -type double3 0.5 0.5 0.5;

#Motion Blur
cmds.setAttr('hardwareRenderingGlobals.motionBlurEnable', 1)
cmds.setAttr('hardwareRenderingGlobals.motionBlurShutterOpenFraction', 0.2)
cmds.setAttr('hardwareRenderingGlobals.motionBlurSampleCount', 16)

#Anti-aliasing
setAttr "hardwareRenderingGlobals.lineAAEnable" 1;
setAttr "hardwareRenderingGlobals.multiSampleEnable" 0;

#Render Option
setAttr "hardwareRenderingGlobals.holdOutMode" 1;
