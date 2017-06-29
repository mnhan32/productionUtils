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


def shotgunInfo(filename):
    
    pwd = os.path.dirname(__file__)
    cfgfile = os.path.join(pwd,'../config/config.cfg')
    f = open(cfgfile)
    config = json.load(f)
    f.close()
    rootPath = config['project'][rootKey]['root']
    sg = Shotgun(config['shotgun']['server'],script_name=config['shotgun']['scriptName'],api_key=config['shotgun']['apiKey'])
    data = filename.split('.')
        
    proj = config['project']['name']
    seq = data[1]
    shotcode = data[2]
    task = data[3]
    version = int(data[4].split('v')[1])
    print proj, seq, shotcode, task
    filterArgs = [
        ["project.Project.name", "is", proj],
        ["entity.Shot.code", "is", shotcode],
        ["entity.Shot.sg_sequence.Sequence.code", "is", seq],
        ["content", "is", task]
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
    data = sg.find('Task', filters=filterArgs, fields=fieldArgs)
    if not data:
        print 'no matching data on shotgun for %s, %s, %s, %s'%(proj, seq, shotcode, task)
        outData={'err':['no matching data on shotgun for %s, %s, %s, %s'%(proj, seq, shotcode, task)]}
        return outData

    shotData  = data[0]
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
    print rootPath
    print outData
    tarfolder = os.path.join(rootPath, outData['proj'])
    tarfolder = os.path.join(tarfolder, 'sequences')
    tarfolder = os.path.join(tarfolder, outData['seq'])
    tarfolder = os.path.join(tarfolder, outData['shot'])
    outData['version'] = version
    outData['shotPath'] = tarfolder
    outData['anmPath'] = os.path.join(tarfolder, outData['step'])
    outData['cfxPath'] = os.path.join(tarfolder,'cfx')
    outData['layPath'] = os.path.join(tarfolder,'lay')
    outData['lgtPath'] = os.path.join(tarfolder,'lgt')
    if not os.path.isdir(outData['shotPath']):
        outData['err'].append('%s not existed.'%outData['shotPath'])
    
    if not os.path.isdir(outData['anmPath']):
        outData['err'].append('%s not existed.'%outData['anmPath'])

    if not os.path.isdir(outData['cfxPath']):
        outData['err'].append('%s not existed.'%outData['cfxPath'])
    
    if outData['headIn'] == None or outData["tailOut"] == None :
        outData['err'].append('head_in & tailout info not completed.')

    return outData
