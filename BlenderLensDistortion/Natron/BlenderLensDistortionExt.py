############################
# by Menghan Ho
# 2017/03/29
# plplug Ext file for Blender Lens Distortion
#
import NatronEngine
import os

def runSync(thisParam, thisNode, thisGroup, app, userEdited):
    
    if thisParam.getScriptName()=='sync':
        dataIn = thisNode.getParam('blenderLensInfo').getValue()
        if dataIn and os.path.isfile(dataIn):
            with open ( dataIn, 'r') as info:
                data = info.readlines()
        if data:
            
            attr=[1,1,1,1,1,1,1,1,1,1]            
            
            for d in data:
                dsplit = d.split(':')
                
                if 'sensor width' in dsplit[0]:
                    param='sensor_width'
                    var = float(dsplit[1])
                    thisNode.getParam(param).setValue(var)
                    attr[0] = 0
                    
                if 'focal length' in dsplit[0]:
                    param='focal_length'
                    var = float(dsplit[1])
                    thisNode.getParam(param).setValue(var)
                    attr[1] = 0

                if 'cx' in dsplit[0]:
                    param='center'
                    var = float(dsplit[1])
                    thisNode.getParam(param).setValue(var,0)
                    attr[2] = 0

                if 'cy' in dsplit[0]:
                    param='center'
                    var = float(dsplit[1])
                    thisNode.getParam(param).setValue(var,1)
                    attr[3] = 0

                if 'model' in dsplit[0]:
                    param='polynomial'
                    if 'DIVISION' in dsplit[1]:		
                        var = 0
                    elif 'POLYNOMIAL' in dsplit[1]:
                        var = 1 
                    thisNode.getParam(param).setValue(var)
                    attr[4] = 0

                if 'k1' in dsplit[0]:
                    param='k'
                    var = float(dsplit[1])
                    thisNode.getParam(param).setValue(var,0)
                    attr[5] = 0

                if 'k2' in dsplit[0]:
                    param='k'
                    var = float(dsplit[1])
                    thisNode.getParam(param).setValue(var,1)
                    attr[6] = 0

                if 'k3' in dsplit[0]:
                    param='k'
                    var = float(dsplit[1])
                    thisNode.getParam(param).setValue(var,2)
                    attr[7] = 0

                if 'p1' in dsplit[0]:
                    param='p_coeff'
                    var = float(dsplit[1])
                    thisNode.getParam(param).setValue(var,0)
                    attr[8] = 0


                if 'p2' in dsplit[0]:
                    param='p_coeff'
                    var = float(dsplit[1])
                    thisNode.getParam(param).setValue(var,1)
                    attr[9] = 0

            #set default
            if attr[0]:                
                thisNode.getParam('sensor_width').setValue(23.76)
            if attr[1]:
                thisNode.getParam('focal_length').setValue(24)
            if attr[2]:
                thisNode.getParam('center').setValue(960.0,0)
            if attr[3]:
                thisNode.getParam('center').setValue(540.0,1)
            if attr[4]:
                thisNode.getParam('polynomial').setValue(1)
            if attr[5]:
                thisNode.getParam('k').setValue(0,0)
            if attr[6]:
                thisNode.getParam('k').setValue(0,1)
            if attr[7]:
                thisNode.getParam('k').setValue(0,2)
            if attr[8]:
                thisNode.getParam('p_coeff').setValue(0,0)
            if attr[9]:
                thisNode.getParam('p_coeff').setValue(0,1)
                            
#end
