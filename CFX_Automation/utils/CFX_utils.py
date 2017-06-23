import os, json

#file name format
# {Proj}.{Seq}.{ShotCode}.{Task}.v##.ma
def fileNameExam(filename):
    data = filename.split('.')
    validate = True

    if not len(data) == 6:
        print 'wrong file name'
        validate = False

    if not data[5] == 'ma':
        print 'wrong file format, require ma, get %s'%data[5]
        validate = False

    versionCheck = data[4].split('v')
    if not len(versionCheck) == 2:
        print 'wrong version format, require (lower case) v##, get %s'%data[4]
        validate = False
   
    if not version[1].isdigit():
        print 'wrong version number, require number, get %s'% version[1]
        validate = False

    if not len(version[1]) == 4:
        print 'wrong version padding, require 4 padding, get %s'% len(version[1])
        validate = False

    return True

#get config
def getConfig(configName, path=None):
    if not path:
        pwd = os.path.dirname(__file__)
    else:
        pwd = path

    if configName == 'proj':
        cfgfile = os.path.join(pwd,'../config/config.cfg')
    elif configName == 'CFX':
        cfgfile = os.path.join(pwd,'../config/CFX_Rig.cfg')
    else:
         cfgfile = os.path.join(pwd,configName)

    try:
        cfgfile = os.path.abspath(cfgfile)
        f = open(cfgfile)
        config = json.load(f)
        f.close()
    except:
        print 'failed in loading config %s'%cfgfile
        return False
    return config

