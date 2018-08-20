sf=1841
ef =2290
fPath='T:/Han/frameRange%s_%s.txt'%(sf,ef)
tmpF = ''
for i in range(sf,ef,2):
    if not i == sf:
        tmpF += ','
    tmpF += str(i)

with open(fPath,'w') as f:
    f.write(tmpF)
