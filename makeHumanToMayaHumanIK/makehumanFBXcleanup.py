from __future__ import print_function
from xml.dom import minidom
import sys,os

try:
    import maya.standalone
    maya.standalone.initialize( name = 'python' )
except:
    pass
import maya.cmds as mc
import maya.mel as mm

mc.loadPlugin('fbxmaya')
mc.loadPlugin('mayaCharacterization')
mc.loadPlugin('mayaHIK')


scriptPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'template')

for i in sys.argv[1:]:
    basename = '.'.join(os.path.basename(i).split('.')[0:-1])
    fileP = os.path.dirname(i)
    mc.file(f=True,new=True)
    fbxIn = 'FBXImport -f "%s"'%'/'.join(i.split('\\'))
    print(fbxIn)
    fbxFile = mm.eval(fbxIn)
    j=mc.ls(typ='joint',l=True)
    m=mc.ls(typ='mesh',ni=True)
    tran = [mc.listRelatives(t,p=True)[0] for t in m]
    
    #TODO define template, maybe by joint number?
    templateName = 'MH_game_engine.xml'
    xmlPath = os.path.join(scriptPath,templateName)    
    
    for k in m:
        sC = mc.listConnections(k,s=True,d=False,t='skinCluster')
        if sC:
            mc.skinCluster(sC[0],e=True,ub=True)
    sj = j
    sj.append(j[0].split('|')[1])
    mc.makeIdentity(sj,apply=True,t=True,r=True,s=True,jo=False)

    [mc.skinCluster(j,k) for k in tran]
    
    rf = mc.file('C:\Users\mnhan\Desktop\woman_2.fbx',r=True,iv=True,gl=True,options='v=0;',namespace=basename,mnc=False)
    
    #rN = mc.referenceQuery(rf,nodes=True)
    #rS = [k for k in rN if mc.listRelatives(k,s=True,type='mesh',fl=True)]
    
    for t in m:
        #print(t)
        sC1 = mc.listConnections(t,s=True,d=False,type='skinCluster')[0]
        ty = '%s:%s'%(basename,t)
        sC2 = mc.listConnections(ty,s=True,d=False,type='skinCluster')[0]
        #print(sC1,sC2)
        mc.copySkinWeights( ss=sC2, ds=sC1,noMirror=True)
    
    mc.file(rf,rr=True)
    
    #human ik
    
    charName = mm.eval('hikCreateCharacter( "Char01" );')
    xmlDoc = minidom.parse(xmlPath)
    itemlist = xmlDoc.getElementsByTagName('item')
    for idx,item in enumerate(itemlist):
        tarbone = item.attributes['value'].value
        if tarbone:
            mm.eval('hikSetCharacterObject("%s","%s",%i,0);'%(tarbone, charName,idx))

    mm.eval('hikSetCurrentCharacter("%s");'%charName)
    mm.eval('hikCreateControlRig();')


    mc.file(rename=os.path.join(fileP,'%s.ma'%basename))
    mc.file(save=True,type='mayaAscii')
    mc.quit(f=True)

