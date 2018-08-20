allC=[i for i in hou.node("/out").children() if i.type().name()=='ifd']
for i in allC:
    pyCmd="import re\ncm=hou.pwd().path()\nval=hou.node(cm).parm('vm_picture').eval()\npmap=hou.hscript('pathmap -ct %s'%val)[0]\nif pmap:\n    sP=re.sub('\\n', '',pmap)\n    pSplit=sP.split('.')\n    pSplit[-2]='%sF4'%'$'\n    finalPath='.'.join(pSplit)\n    hou.node(cm).parm('vm_picture').set(finalPath)"
    i.parm('prerender').set(pyCmd)
    i.parm('lprerender').set('python')
