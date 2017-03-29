import os
myRoot = nuke.thisNode()
dataIn=myRoot['blenderLensData'].getValue()
if os.path.isfile(dataIn):
	with open ( dataIn, 'r') as info:
		data = info.readlines()

for d in data:
	dsplit = d.split(':')
	
	if 'sensor width' in dsplit[0]:
		param='Sensor Size'
		var = float(dsplit[1])
		myRoot[param].setValue(var)

	if 'focal length' in dsplit[0]:
		param='Focal Length'
		var = float(dsplit[1])
		myRoot[param].setValue(var)


	if 'cx' in dsplit[0]:
		param='Center'
		var = float(dsplit[1])
		myRoot[param].setValue(var,0)


	if 'cy' in dsplit[0]:
		param='Center'
		var = float(dsplit[1])
		myRoot[param].setValue(var,1)

	if 'model' in dsplit[0]:
		param='Polynomial'
		if 'DIVISION' in dsplit[1]:		
			var = 0
		elif 'POLYNOMIAL' in dsplit[1]:
			var = 1 
		myRoot[param].setValue(var)

	if 'k1' in dsplit[0]:
		param='k'
		var = float(dsplit[1])
		myRoot[param].setValue(var,0)


	if 'k2' in dsplit[0]:
		param='k'
		var = float(dsplit[1])
		myRoot[param].setValue(var,1)


	if 'k3' in dsplit[0]:
		param='k'
		var = float(dsplit[1])
		myRoot[param].setValue(var,2)


	if 'p1' in dsplit[0]:
		param='p'
		var = float(dsplit[1])
		myRoot[param].setValue(var,0)

	if 'p2' in dsplit[0]:
		param='p'
		var = float(dsplit[1])
		myRoot[param].setValue(var,1)

	
		


