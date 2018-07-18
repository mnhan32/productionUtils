# -*- coding: utf-8 -*-


#---------------------------------------
#scrript name : makeTxTool.py
#                by Meng-Han Ho
#                2016/04/03
#---------------------------------------
#version: beta 0.9
#
#    very first version of makeTx tool
#    this script uses maketx to convert texture
#    to mipmap tx format.
#
#---------------------------------------
#This scripts works inside Maya, 
#or as standalong python script
#
#for Maya, including script folder to PYTHON env 
#OIIO folder is alos crucial, since we are using maketx and oiiotool 
#for standalong version, 
#make sure that you have QT4.8.6 ,Python 2.7, and Pyside ready
#then just run the python script
#---------------------------------------
#
#    TO DO
#    the code is messy, need to clean up and optimized.
#


import sys,os,glob,platform,time
import UI_makeTx as maketxUI
reload(maketxUI)
#from PySide.QtCore import *
#from PySide.QtGui import *
from subprocess import call

try:
    import maya.cmds as cmds
    mayaVersion = cmds.about(v=True)

    class mtx_standalong(object):
        def __init__(self):
            self.standalong = True
    
except:
    #print 'STANDALONG'
    from PySide.QtCore import *
    from PySide.QtGui import *
    #from PySide.QtUiTools import *
    #from shiboken import wrapInstance
    class mtx_standalong(object):
        def __init__(self):
            self.standalong = False
            
mayaModeStatus = mtx_standalong()

if mayaModeStatus.standalong:    
    import maya.cmds as cmds
    import maya.OpenMayaUI as omui    
    if int(mayaVersion) >= 2017:
        from PySide2.QtGui import *
        from PySide2.QtCore import *
        from PySide2.QtWidgets import *
        #from PySide2.QtUiTools import *
        from shiboken2 import wrapInstance
    else:
        from PySide.QtGui import *
        from PySide.QtCore import *
        #from PySide.QtUiTools import *
        from shiboken import wrapInstance
    #import makeTxMayaMod as modm
    #print 'LOADED!'
    def doIt():
        global myWin
        try:
            myWin.close()
        except: pass
        myWin = MainWindow(maya_main_window())
        myWin.show()

    def maya_main_window():
        main_window_ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(long(main_window_ptr), QWidget)
        
class MainWindow(QMainWindow, maketxUI.Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.tabWid.setTabEnabled(2, mayaModeStatus.standalong)

        #os
        cmdName = 'maketx'
        self.runningOS = 'linux'
        os_platform = platform.system()
        if 'windows' in os_platform.lower() or 'win' in os_platform.lower():
            cmdName = 'maketx.exe'
            self.runningOS = 'windows'
        elif 'darwin' in os_platform.lower():
            self.runningOS = 'mac'

        #TO DO
        #check if when py is running by other software, __file__ will return different path
        cmdDir = os.path.dirname(os.path.abspath(__file__))
        cmdDir = os.path.join(cmdDir,'OpenImageIO-1.5.0-OCIO')
        cmdDir = os.path.join(cmdDir,'bin')
        self.cmdDefaultPath = os.path.join(cmdDir,cmdName)
        self.cmdPath = self.cmdDefaultPath
        if os.path.isfile(self.cmdPath):
            self.lE_cmdPath.setText(self.cmdPath)
        else:
            self.writeToLog('no default maketx command existd!')
        self.tB_sourceCmbBrowse.clicked.connect(lambda: self.showCmdBrowser(self,self.lE_cmdPath))
        self.defaultCmdFlag ='-u -oiio'
        self.cmdFlag = self.defaultCmdFlag
        self.lE_cmdFlag.setText(self.defaultCmdFlag)

        self.gB_commandFlags.clicked.connect(self.updateCmdFlag)

        #filetype filter
        self.defaultImageExt = [str(x) for x in self.lE_imageFilter.text().split(' ')]
        self.ext=self.defaultImageExt
        self.updateImageFilter(self,self.gB_imageFilter,self.lE_imageFilter,'defaultImageExt','ext')
        self.gB_imageFilter.clicked.connect(lambda: self.updateImageFilter(self,self.gB_imageFilter,self.lE_imageFilter,'defaultImageFilter','ext'))
        self.lE_imageFilter.textChanged.connect(lambda: self.updateImageFilter(self,self.gB_imageFilter,self.lE_imageFilter,'defaultImageFilter','ext'))
        self.tabWid.setCurrentIndex(0)

        #store settings
        self.sourceDir = ''
        self.tarDir = ''
        self.cTab = self.tabWid.currentIndex()

        #source folder
        self.tB_sourceDirBrowse.clicked.connect(lambda: self.showDirBrowser(self,self.cmB_sourceDirPath))
        #tar folder
        self.tB_tarDirBrowse.clicked.connect(lambda: self.showDirBrowser(self,self.cmB_tarDirPath))

        #source files
        self.tB_sourceFileBrowse.clicked.connect(lambda: self.showFilesBrowser(self,self.lW_sourceFiles))
        self.tB_clearList.clicked.connect(lambda: self.clearFileList(self, self.lW_sourceFiles))
        self.tB_removeSel.clicked.connect(lambda: self.removeSelFromList(self,self.lW_sourceFiles))

        #if dir change, validate path
        self.cmB_sourceDirPath.currentIndexChanged.connect(lambda: self.pB_dirAction(self,self.cmB_sourceDirPath,'sourceDir'))
        self.cmB_tarDirPath.currentIndexChanged.connect(lambda: self.pB_dirAction(self,self.cmB_tarDirPath,'tarDir'))

        #convert all and subfolder option
        self.subFolder = self.cB_subFolder.isChecked()
        self.subLevel = self.sB_subLevel.value()

        self.cB_subFolder.toggled.connect(lambda: self.checkBoxStateChange(self, self.cB_subFolder, 'subFolder'))
        self.sB_subLevel.valueChanged.connect(lambda: self.sBValueChange(self,self.sB_subLevel,'subLevel'))

        #removal
        self.removal=False
        self.overwrite=False
        self.gB_overwrite.clicked.connect(lambda: self.checkBoxStateChange(self,self.gB_overwrite, 'removal'))
        self.cB_overwrite.clicked.connect(lambda: self.checkBoxStateChange(self,self.cB_overwrite, 'overwrite'))
        self.pB_deleteTx.clicked.connect(self.removeExistTx)

        #oiio
        oiioName = 'oiiotools'
        if self.runningOS=='windows':
            oiioName = 'oiiotool.exe'
            
        self.oiioCmd = os.path.join(cmdDir,oiioName)
        if os.path.isfile(self.oiioCmd):
            self.gB_extra.setEnabled(True)
        else:
            self.gB_extra.setEnabled(False)
            self.oiioCmd=''
            pass

        self.extra=False
        self.suffix=''
        self.oiioFlag=''
        self.gB_extra.setChecked(self.extra)
        self.gB_extra.clicked.connect(lambda:self.checkBoxStateChange(self,self.gB_extra,'extra'))
        self.lE_suffix.textChanged.connect(lambda: self.lineEditTextChanged(self, self.lE_suffix,'suffix'))
        self.lE_oiioFlag.textChanged.connect(lambda: self.lineEditTextChanged(self, self.lE_oiioFlag,'oiioFlag'))
        self.pB_goOiio.clicked.connect(self.oiioGo)

        #maya related
        self.mayaConvertAll = True
        self.mayaAutoSwap = False
        self.PROCESS_NODE=[]
        self.rB_allShd.toggled.connect(lambda: self.checkBoxStateChange(self,self.rB_allShd,'mayaConvertAll'))
        self.cB_swapToTx.clicked.connect(lambda: self.checkBoxStateChange(self,self.cB_swapToTx,'mayaAutoSwap'))
        self.pB_toTx.clicked.connect(lambda: self.swapTx(self,True))
        self.pB_toNonTx.clicked.connect(lambda: self.swapTx(self,False))
        #menu
        #about
        # cmd flag
        self.ac_aboutMakeTx.triggered.connect(lambda: self.showCmdHelp(self,'https://manned.org/oiiotool.1'))
        self.ac_aboutOIIO.triggered.connect(lambda: self.showCmdHelp(self,'https://manned.org/maketx.1'))
        self.ac_aboutMe.triggered.connect(self.showAbout)

        self.ac_createBatchFile.triggered.connect(self.createBatchFile)

        self.ac_quit.triggered.connect(self.close)

        #if tab Change
        self.tabWid.currentChanged.connect(self.currentTab)

        #do it button
        self.pB_doMakeTx.clicked.connect(self.maketxGo)
        #show ui
        self.show()
        
    def oiioGo(self):
        oiioCmdList = self.genOiioCmd()
        if oiioCmdList:
            #print oiioCmdList
            for x in oiioCmdList:
                call(x)
                
    def genOiioCmd(self):
        if self.oiioCmd:
            #you have oiio cmd in where maketx is located
            oiioCmdList = []
            sourceF = self.generateOutputList()
            #print sourceF
            if sourceF and self.oiioFlag:
                for i in sourceF:                
                    oiioCmd1 = [str(self.oiioCmd)]
                    oiioCmd2 = [i]
                    dirN = os.path.dirname(i)
                    baseNameExtract = os.path.basename(i).split('.')[0:-1]
                    extName = os.path.basename(i).split('.')[-1]
                
                baseName = ''
                #print len(baseNameExtract)
                if len(baseNameExtract)>1:
                    for x in baseNameExtract:
                        baseName += i
                elif len(baseNameExtract)==1:
                    #print baseNameExtract[0]
                    baseName = baseNameExtract[0]
                else:
                    pass

                oiioCmd3 = [str(x) for x in self.oiioFlag.split(' ') if x.strip()!='']
                oiioCmd4 = ['-o']
                if self.suffix.strip()!='':
                    tarFile = os.path.join(dirN, (baseName+'_'+str(self.suffix)+'.'+extName))
                else:
                    tarFile = i

                oiioCmd5 = [tarFile]
                oiioCmdList.append((oiioCmd1 + oiioCmd2+oiioCmd3+oiioCmd4+oiioCmd5))
                return oiioCmdList
            else:
                self.writeToLog('no valid output list or command flag.')
                return False
                
    def lineEditTextChanged(self,*arg):
        setattr(self,arg[2],arg[1].text())
        
    def updateImageFilter(self,*arg):
        if arg[1].isChecked:
            setattr(self,arg[4],[str(x) for x in arg[2].text().split(' ') if x.strip() != ''])
        else:
            setattr(self,arg[4],[x for x in getattr(self,arg[3]) if x.strip()!=''])

    def removeExistTx(self):
        genList = self.generateOutputList()
        #print genList
        if genList:
            for x in genList:
                dirN = os.path.dirname(x)
                baseNameExtract = os.path.basename(x).split('.')[0:-1]
                baseName = ''
                #print len(baseNameExtract)
                if len(baseNameExtract)>1:
                    for x in baseNameExtract:
                        #print x
                        baseName += x                       
                elif len(baseNameExtract)==1:
                    print baseNameExtract[0]
                    baseName = baseNameExtract[0]
                else:
                    break
                #print 'remove', baseName
                txFileName = os.path.join(dirN,(baseName+'.tx'))
                if os.path.isfile(txFileName):
                    try:
                        os.remove(txFileName)
                    except:
                        self.writeToLog('Failed to delete '+txFileName)
                #print 'another location'
                if self.gB_saveTo.isChecked:
                    if self.tarDir != False and self.tarDir.strip()!='':
                        extraFile = os.path.join(self.tarDir,(baseName+'.tx'))
                        if os.path.isfile(extraFile):
                            try:
                                os.remove(extraFile)
                            except:
                                self.writeToLog('Failed to delete'+extraFile)

    def sBValueChange(self,*arg):
        setattr(self,arg[2],arg[1].value())

    def checkBoxStateChange(self,*arg):
        if arg[1].isChecked():
            setattr(self,arg[2],True)
        else:
            setattr(self,arg[2],False)

    def updateCmdFlag(self):
        if self.gB_commandFlags.isChecked():
            newFlg = self.lE_cmdFlag.text()
            self.cmdFlag = newFlg
        else:
            self.cmdFlg = self.defaultCmdFlag

    def currentTab(self):
        try:
            self.cTab = self.tabWid.currentIndex()
        except:
            print 'return currentTab fail'
            pass

    def removeSelFromList(self,*arg):
        selMe = arg[1].selectedItems()
        for i in selMe:
            arg[1].takeItem(arg[1].row(i))

    def clearFileList(self,*arg):
        arg[1].clear()

    def showCmdBrowser(self,*arg):
        fName = QFileDialog.getOpenFileName(self,'maketx cmd',self.cmdPath)
        if fName[0]:
            arg[1].setText(fName[0])
            self.cmdPath = fName[0]

    def browserImageFilter(self):
        imageFilter = 'Image Files ('
        for x in self.ext:
            imageFilter += '*.'
            imageFilter += x
            imageFilter += ' '
        imageFilter += ')'
        #print imageFilter
        return imageFilter

    def showFilesBrowser(self,*arg):
        imageFilter = self.browserImageFilter()

        fName = QFileDialog.getOpenFileNames(self,'Select Files','',imageFilter)
        if fName[0]:
            try:
                #for selected list view
                for f in range(len(fName[0])):
                    countItem = arg[1].count()
                    addSwitch = 1
                    for x in range(countItem):
                        test = arg[1].item(x).text()
                        if test == str(fName[0][f]):
                            addSwitch = 0
                        else:
                            pass
                    if addSwitch==1:
                        #
                        #if arg[1].findText(fName[0][f]):
                        #    print 'the same'
                        #print fName[0][f]
                        try:
                            arg[1].insertItem(countItem, fName[0][f])
                        except:
                            print 'no add'
                        arg[1].item(countItem).setText(fName[0][f])
                        countItem = arg[1].count()
                        
            except:
                pass

    def showDirBrowser(self,*arg):
        #fName = QFileDialog.getExistingDirectory(self,'Open Dir','')
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.DirectoryOnly)
        dlg.setOptions(QFileDialog.DontUseNativeDialog)
        dlg.setNameFilter(self.browserImageFilter())
        fName = False
        if dlg.exec_():
            fName = dlg.selectedFiles()

        if fName:
            try:
            #only add item if text not in list,
            #else, if text found, simply switch to item
                dirIndex = arg[1].findText(fName[0])
                if dirIndex < 0:
                    arg[1].insertItem(arg[1].count(),fName[0])
                    arg[1].setCurrentIndex(arg[1].count()-1)
                else:
                    #print fName,' : ',dirIndex
                    arg[1].setCurrentIndex(dirIndex)
            except:
                pass
        else:
            #no valid dir
            self.writeToLog('Escape folder selection.')

    def getCurrentDirPath(self):
        return self.cmB_dirPath.currentText()

    def writeToLog(self,inputLog):
        #self.lE_log.setText(inputLog)
        pass

    def validateDir(self,*arg):
        fPath = arg[1].currentText()
        validPath = os.path.abspath(fPath)
        if os.path.isdir(fPath)!= True:
            arg[1].removeItem(arg[1].currentIndex())
            validPath = False
            self.writeToLog(fPath + 'is not a valid dir path!')
        else:
            if fPath != validPath:
                arg[1].setItemText(arg[1].findText(fPath),validPath)

        return validPath

    def pB_dirAction(self,*arg):
        result = self.validateDir(self,arg[1])
        setattr(self,arg[2],result)

    def globFolderAll(self,*arg):
        return [x[0] for x in os.walk(arg[1])]

    def globFolder(self,*arg):
        outFolder=[]
        top = arg[1]
        outFolder.append(top)
        startinglevel = top.count(os.sep)

        for top, dirs, files in os.walk(top):
              level = top.count(os.sep) - startinglevel
              if level<arg[2]:
                  for d in dirs:
                      if d:
                        outFolder.append(os.path.join(top,d))
        return outFolder

    def globFolderFiles(self,*arg):
        fileList = []
        #print self.ext
        for x in self.ext:
            #print x
            fFilter = '*.'+x
            globDir = os.path.join(arg[1],fFilter)
            globFiles = glob.glob(globDir)
            if globFiles:
                [fileList.append(str(imageFile)) for imageFile in globFiles]
        return fileList

    def outListFromFolder(self):
        processFolder = self.sourceProcessFolder()
        if processFolder != False:
            processFiles = []
            for p in processFolder:
                filesInFolder = self.globFolderFiles(self,p)

                [processFiles.append(i) for i in filesInFolder if i.strip()!='']
            return processFiles
        else:
            return False

    def outListFromListView(self,*arg):
        return [arg[1].item(i).text() for i in range(arg[1].count())]

    def outListFromMaya(self):
        if self.mayaConvertAll:
            outList = self.returnAllTextureList()
        else:
            outList = self.returnTextureListFromSelect()
        return outList


    def generateOutputList(self):
        if self.cTab == 0:
            outList = self.outListFromFolder()
            #print 'here',outList
        elif self.cTab == 1:
            outList = self.outListFromListView(self,self.lW_sourceFiles)
        elif self.cTab == 2:
            outList = self.outListFromMaya()

        if outList:
            return outList
        else:
            return False

    def sourceProcessFolder(self):
        if self.sourceDir != False and self.sourceDir.strip()!='':
            if self.subFolder == False:
                processFolder = self.globFolderAll(self,self.sourceDir)
            else:
                processFolder = self.globFolder(self,self.sourceDir,self.subLevel)
            return processFolder
        else:
            return False

    def generateDesList(self,*arg):
        if arg[1]:
            desList = []
            for x in arg[1]:
                baseNameExtract = os.path.basename(x).split('.')[0:-1]
                baseName = ''
                if len(baseNameExtract)>1:
                    for i in baseNameExtract:
                        baseName += i
                        #baseName +='.'
                elif len(baseNameExtract)==1:
                    baseName = baseNameExtract[0]
                else:
                    return False
                    
                #print 'create ' , baseName
                if self.gB_saveTo.isChecked():
                    if self.tarDir != False and self.tarDir.strip() != '':
                        desList.append(os.path.join(self.tarDir, baseName+'.tx'))
                    else:
                        desList.append(os.path.join(os.path.dirname(x),(baseName+'.tx')))
                else:
                    desList.append(os.path.join(os.path.dirname(x),(baseName+'.tx')))
            return desList
        else:
            return False

    def genBatchList(self):
        sourceF = self.generateOutputList()
        #print sourceF
        if sourceF:
            tarF = self.generateDesList(self,sourceF)
            #print 'batch list ', tarF
            if tarF:
                batchList = []
                for x in range(len(sourceF)):
                    batchCmd = self.cmdPath
                    batchFlag = self.cmdFlag.split(' ')
                    batchSource = sourceF[x]
                    batchOutFlag = '-o'
                    batchTar = tarF[x]
                    #overwrite?
                    if os.path.isfile(batchTar):
                        if self.removal and self.overwrite:
                            batchCmdList = [batchCmd]+batchFlag+[batchSource,batchOutFlag,batchTar]
                            batchList.append(batchCmdList)

                    else:
                        batchCmdList = [batchCmd]+batchFlag+[batchSource,batchOutFlag,batchTar]
                        batchList.append(batchCmdList)


                if batchList:
                    return batchList
                else:
                    return False
            else:
                return False
        else:
            return False

    def showCmdHelp(self,*arg):
        #print 'cmd help'
        #QDesktopServices.openUrl(QUrl("https://support.solidangle.com/display/ARP/maketx"))
        try:
            import webbrowser
            webbrowser.open(arg[1])
        except:
            self.writeToLog(arg[1])
            pass

    def showAbout(self):
        aboutText = 'maketx gui beta \r\n'
        aboutText +='by Meng-Han Ho\r\n'
        aboutText +='mnhan32@gmail.com\r\n'
        QMessageBox.information(self,'About',aboutText )
        pass

    def createBatchFile(self):
        #open file and write
        batchExt = 'sh'
        if self.runningOS=='windows':
            batchExt = 'bat'
            fileFilter = ('Windows Batch (*.'+batchExt+')')
        else:
            fileFilter = ('Shell Script (*.'+batchExt+')')
        
        cmdList = self.genBatchList()
            
        if cmdList:
            
            fName = QFileDialog.getSaveFileName(self,'Save Batch File','',fileFilter)

            if fName[0]:
                
                pass
            else:
                self.writeToLog('failed to select output batch file.')
                return False
            
        
            try:
                if os.path.basename(fName[0]).split('.')[1]:
                    fileToSave = fName[0]
            except:
                fileToSave = str(fName[0])+'.'+batchExt


            batToWrite = open(fileToSave,'wb')
            if self.runningOS == 'windows':
                headLine = 'REM Maketx Generate Script for Windows\r\n'
                endLine = '\r\nPASUE'
            else:
                headLine = '#!/bin/bash\n'
                endLine = '\n #end of script'

            writeData = headLine
            for x in cmdList:
                #print 'x : ' , x
                lineToWrite = ''
                for i in x:
                    lineToWrite += i
                    lineToWrite += ' '

                if self.runningOS == 'windwos':
                    lineToWrite +='\r\n'
                else:
                    lineToWrite += '\n'
                writeData += lineToWrite

            writeData += endLine
            batToWrite.write(writeData)

            batToWrite.close()
        else:
            QMessageBox.information(self,'Information','There are no files need to be converted.')
            self.writeToLog('no valid files to be converted.')
            return False

    def maketxGo(self):
        #print 'go'
        cmdList = self.genBatchList()
            #msgBox.setText('Convert')        
        if cmdList:
            switch = True
            if self.ac_confirm.isChecked():
                confirmText = 'You are about to convert %s files to tx. Are you Sure?'%len(cmdList)
                msgBox = QMessageBox.question(self,'confirmation',confirmText,QMessageBox.StandardButton.No,QMessageBox.StandardButton.Yes)
            
                if msgBox ==QMessageBox.StandardButton.Yes:
                    switch = True
                else:
                    switch = False
                
            if switch:
                print cmdList
                for x in cmdList:
                    call(x,shell=True)
                
                if self.cTab == 2:
                    if self.mayaAutoSwap:
                        if self.PROCESS_NODE:
                            print 'here'
                            self.setNewTextureFilename()
            else:
                self.writeToLog('Job abort')
        else:
            QMessageBox.information(self,'Information','There are no files need to be converted.')
    
    def recursiveToConnectionEnd(self,mode,matchNode,matchType,inputSel,loopLimit,loopCount):
        if mode:
            sConn = True
            dConn = False
        else:
            sConn = True
            dConn = True
        if loopCount<loopLimit:
            #print 'LOOP ITEM : ',inputSel     
            for i in range(len(inputSel)):
                #print i, len(inputSel) 
                cO =cmds.listConnections(inputSel[i],s=True,d=False)       
                if cO:
                    connection = list(set(cO)) 
                    [self.PROCESS_NODE.append(x) for x in connection if cmds.nodeType(x) in matchType]              
                    loopCount=loopCount+1
                    self.recursiveToConnectionEnd(mode,matchNode,matchType,connection,loopLimit,loopCount)
                else:
                    if i == len(inputSel)-1:                 
                        break
        else:
            pass


    def returnTextureListFromSelect(self):
        sel = cmds.ls(sl=True,l=True)
        fileNode = []
        fileNodeType = ['file']
        selGrp = sel
        safeRecursiveLimit = 100
        self.PROCESS_NODE = []
        for x in sel:
           if cmds.attributeQuery('outColor',node=x,exists=True):
               if len(cmds.listConnections(x+'.outColor',s=False,d=True,t='shadingEngine'))>0:
                   selGrp = selGrp + cmds.listConnections(x+'.outColor',s=False,d=True,t='shadingEngine')
                   selGrp.remove(x)
        self.recursiveToConnectionEnd(1,fileNode,fileNodeType,selGrp,safeRecursiveLimit,0)
        self.PROCESS_NODE = list(set(self.PROCESS_NODE))
        outList = []
        for x in self.PROCESS_NODE:
            try:
                tF = cmds.getAttr(x+'.fileTextureName')
                if os.path.isfile(os.path.abspath(str(tF))):
                    outList.append(str(os.path.abspath(tF)))
            except:
                pass
        if outList:
            return list(set(outList))
        else:
            return False
            
    def returnAllTextureList(self):
        fileNodeType = ['file']
        self.PROCESS_NODE = []
        for x in fileNodeType:
            if cmds.ls(l=True,type=x):
                [self.PROCESS_NODE.append(i) for i in cmds.ls(l=True,type=x)]
                
        self.PROCESS_NODE = list(set(self.PROCESS_NODE))
        outList = []
        for x in self.PROCESS_NODE:
            try:        
                tF = cmds.getAttr(x+'.fileTextureName')
                if os.path.isfile(os.path.abspath(str(tF))):
                    outList.append(str(os.path.abspath(tF)))
            except:
                pass
        if outList:
            return list(set(outList))
        else:
            return False
        
    def setNewTextureFilename(self):
        self.PROCESS_NODE = list(set(self.PROCESS_NODE))
        missingNode = []
        for x in self.PROCESS_NODE:
            try:        
                tF = cmds.getAttr(x+'.fileTextureName')
                baseNameExtract = os.path.basename(tF).split('.')[0:-1]
                baseName = ''
                if len(baseNameExtract)>1:
                    for i in baseNameExtract:
                        baseName += i
                elif len(baseNameExtract)==1:
                    baseName = baseNameExtract[0]
                #print baseName
                tarTx = ''
                if os.path.basename(tF).split('.')[-1]!='tx':
                    if os.path.isfile(os.path.abspath(str(tF))):
                        if self.gB_saveTo.isChecked():
                            if self.tarDir != False and self.tarDir.strip() != '':
                                tarTx = os.path.join(self.tarDir, (baseName+'.tx'))
                            else:
                                tarTx = os.path.join(os.path.dirname(tF),(baseName+'.tx'))
                        else:
                            tarTx = os.path.join(os.path.dirname(tF),(baseName+'.tx'))
                        
                        if os.path.isfile(os.path.abspath(tarTx)):
                            cmds.setAttr(x+'.fileTextureName',os.path.abspath(tarTx),type='string')
                        else:
                            print 'NODE:', x, 'Texture:', os.path.abspath(tarTx),' not existed.'
                            self.writeToLog(('NODE:', x, 'Texture:', os.path.abspath(tarTx),' not existed.'))
            except:
                self.writeToLog(('NODE:', x, ' Failed'))
                pass
        
    def swapTx(self,*arg):
        self.outListFromMaya()
        self.PROCESS_NODE
        if arg[1]:
            self.setNewTextureFilename()
        else:
            self.swapBack()
    
    def swapBack(self):    
        for x in self.PROCESS_NODE:
            try:        
                tF = cmds.getAttr(x+'.fileTextureName')
                baseNameExtract = os.path.basename(tF).split('.')[0:-1]
                baseName = ''
                if len(baseNameExtract)>1:
                    for i in baseNameExtract:
                        baseName += i
                elif len(baseNameExtract)==1:
                    baseName = baseNameExtract[0]
                #print baseName
                tarTx=''
                if os.path.basename(tF).split('.')[-1]=='tx':
                    if os.path.isfile(os.path.abspath(str(tF))):
                        for e in self.ext:
                            tarFile = os.path.join(os.path.dirname(tF),(baseName+'.'+e))
                            if os.path.isfile(os.path.abspath(tarFile)):
                                cmds.setAttr(x+'.fileTextureName',str(os.path.abspath(tarFile)),type='string')
                                break;
                        else:
                            print 'NODE:', x, 'Texture:', os.path.abspath(tarTx),' not existed.'
                            self.writeToLog(('NODE:', x, 'Texture:', os.path.abspath(tarTx),' not existed.'))
            except:
                self.writeToLog(('NODE:', x, ' Failed'))
                pass
            
        

if __name__=='__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)                
