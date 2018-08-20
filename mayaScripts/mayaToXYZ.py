outPath = 'B:/trackInfo.txt'
# start time of playback
start = cmds.playbackOptions(q= 1, min= 1)
# end time of playback
end = cmds.playbackOptions(q= 1, max= 1)
#locators list
locList = cmds.ls(sl= 1)
if len(locList) > 0:
    try:
        # create/open file path to write
        outFile = open(outPath, 'w')
    except:
        cmds.error('file path do not exist !')
    # info to write in
    infoStr = ''
    # start recoard
    for frame in range(int(start), int(end + 1)):
        # move frame
        cmds.currentTime(frame, e= 1)
        # if you need to add a line to write in frame number
        infoStr += str(frame) + '\n'
        # get all locators
        for loc in locList:
            # if you need to add a line to write in locator name
            #infoStr += loc + '\n'
            # get position
            pos = cmds.xform(loc, q= 1, t= 1, ws= 1)
            # write in locator pos
            infoStr += str(pos[0]) + ' ' + str(pos[1]) + ' ' + str(pos[2]) + ' ' + '\n'
    # file write in and close
    outFile.write(infoStr)
    outFile.close()
else:
    cmds.warning('select at least one locator')
