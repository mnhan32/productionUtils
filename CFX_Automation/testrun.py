#from utils import CFX_shotgunInfo
'''
import json
result = CFX_shotgunInfo.shotgunInfo('TGB.demo.demo_0040.animation.v01.mb')
print result
'''
#from utils import CFX_utils

#print CFX_utils.getConfig('proj')
'''
import datetime

timestamp = datetime.datetime.now().strftime("%Y_%m_%d.%H_%M_%S")
logfile = '%s.log'%timestamp
print logfile


a = [1,2,3,4,5]
print a[-3:]
'''


'''
ff = 'T:\\Han\\productionUtils\\CFX_Automation\\config\\CFX_Rig.cfg'
f = open(ff)
config = json.load(f)
f.close()
print config
'''
'''
ab= ['animCurveTA', 'animCurveTL','animCurveTT','animCurveTU']
dw = 'D:\\testTGB\\test.cfg'
fk = open(dw, 'w')
json.dump(ab, fk)
fk.close()
'''

aa = [0,1,2]
print aa[-1]
