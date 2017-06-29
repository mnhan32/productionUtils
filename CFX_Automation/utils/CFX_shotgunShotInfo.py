import sys, os,  json
import CFX_utils

projConfig = CFX_utils.getConfig('proj')
rootKey = "win"
if sys.platform == "linux" or sys.platform == "linux2":
    rootKey = "linux"
elif sys.platform == "darwin":
    # MAC OS X
    rootKey = "darwin"
shotgunAPI = os.path.join(projConfig['project'][rootKey]['utils'], 'shotgunAPI')
sys.path.append(shotgunAPI)

from shotgun_api3 import Shotgun


def shotgunShotInfo(shotcode, task):
    
    rootPath = projConfig['project'][rootKey]['root']
    sg = Shotgun(projConfig['shotgun']['server'],script_name=projConfig['shotgun']['scriptName'],api_key=projConfig['shotgun']['apiKey'])
    proj = projConfig['project']['name']

    seq = [i[:-4] for i in shotcode]

    filterArgs = [
        ["project.Project.name", "is", proj],
        ["entity.Shot.code", "in", shotcode],
        ["entity.Shot.sg_sequence.Sequence.code", "in", seq],
        ["content", "in", task]
     ]
    fieldArgs=[
        "id",
        "content",
        "step.Step.short_name",
        "entity.Shot.sg_head_in", 
        "entity.Shot.sg_tail_out",
        "entity.Shot.sg_cut_in",
        "entity.Shot.sg_cut_out",
        "project.Project.id",
        "project.Project.name",
        "entity.Shot.sg_sequence.Sequence.code",
        "entity.Shot.sg_sequence.Sequence.id",
        "entity.Shot.code",
        "entity.Shot.id"
        ]
    #get task data
    #print filterArgs
    data = sg.find('Task', filters=filterArgs, fields=fieldArgs)

    shotgunData={}
    if not data:
        print 'no matching data on shotgun for %s, %s, %s, %s'%(proj, seq, shotcode, task)
        outData={'err':['no matching data on shotgun for %s, %s, %s, %s'%(proj, seq, shotcode, task)]}
        return outData
    
    for i in data:
        shotData  = i
        outData = {
            "task" : shotData["content"],
            "taskId" : shotData["id"],
            "step" : shotData["step.Step.short_name"],
            "shot" : shotData["entity.Shot.code"],
            "shotId" : shotData["entity.Shot.id"],
            "seq" : shotData["entity.Shot.sg_sequence.Sequence.code"],
            "seqId" : shotData["entity.Shot.sg_sequence.Sequence.id"],
            "proj" : shotData["project.Project.name"],
            "projId" : shotData["project.Project.id"],
            "headIn" : shotData["entity.Shot.sg_head_in"],
            "tailOut" : shotData["entity.Shot.sg_tail_out"],
            "cutIn" : shotData["entity.Shot.sg_cut_in"],
            "cutOut" : shotData["entity.Shot.sg_cut_out"]
        }
        tarfolder = os.path.join(rootPath, outData['proj'])
        tarfolder = os.path.join(tarfolder, 'sequences')
        tarfolder = os.path.join(tarfolder, outData['seq'])
        tarfolder = os.path.join(tarfolder, outData['shot'])
        #outData['version'] = version
        outData['shotPath'] = tarfolder
        outData['anmPath'] = os.path.join(tarfolder, outData['step'])
        outData['cfxPath'] = os.path.join(tarfolder,'cfx')
        outData['layPath'] = os.path.join(tarfolder,'lay')
        outData['lgtPath'] = os.path.join(tarfolder,'lgt')
        if not os.path.isdir(outData['shotPath']):
            outData['errShotPath']=('%s not existed.'%outData['shotPath'])
        
        if not os.path.isdir(outData['anmPath']):
            outData['errAnmPath']=('%s not existed.'%outData['anmPath'])

        if not os.path.isdir(outData['cfxPath']):
            outData['errCfxPath']=('%s not existed.'%outData['cfxPath'])
        
        if outData['headIn'] == None or outData["tailOut"] == None :
            outData['errFrameRange']=True
        
        keyVal = '_'.join([outData['shot'], outData['task']])
        shotgunData[keyVal] = outData
    return shotgunData