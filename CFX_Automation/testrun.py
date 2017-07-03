'''
from utils import CFX_shotgunInfo

import json
a = ['os0040', 'os0010']
b = ['aniTiger', 'aniTiger' ]
CFX_shotgunInfo.shotgunInfo(a, b)
'''
#print result

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
'''
import os
a = ['D:\\', 'testTGB', 'a']
print os.path.join(*a)
'''
a = 'aniTiger_v04.ma'
a.split('_').insert(-1, 'extended')
print a
