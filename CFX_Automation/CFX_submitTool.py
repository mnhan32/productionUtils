import os, sys, json, fnmatch
from PySide import QtCore, QtGui
from ui import ui_CFX_SmedgeSubmit as baseUI
from ui import ui_CFX_ValidationList as validationUI
reload(baseUI)
reload(validationUI)
from utils import CFX_utils, CFX_shotgunShotInfo

projConfig = CFX_utils.getConfig('proj')

rootKey = "win"
if sys.platform == "linux" or sys.platform == "linux2":
    rootKey = "linux"
elif sys.platform == "darwin":
    # MAC OS X
    rootKey = "darwin"

projName = projConfig['project']['name']
projRoot = projConfig['project'][rootKey]['root']
projPath = os.path.join(projRoot, projName)

class CFX_SubmitTool(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(CFX_SubmitTool, self).__init__(parent)
        self.ui = baseUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.__usrFolder = os.path.expanduser("~")
        self.__usrDataPath = os.path.join(self.__usrFolder, ".CFX_sumbitTool")
        self.__usrConfigPath = os.path.join(self.__usrDataPath, 'CFX_submitter.cfg')
        self.__usrConfig = {}
        self.__usrConfig["defaultRoot"] = self.__usrFolder
        self.__errFileName = []


        if not os.path.isdir(self.__usrDataPath):
            self.__genDefault()
        if not os.path.isfile(self.__usrConfigPath):
            self.__genConfig()
        else:
            self.__loadConfig()

        self.__setRootPath(self.__usrConfig["defaultRoot"])
        self.__overwriteExist = False
        self.__showValidation = True
        self.ui.lineEdit.setText(self.__usrConfig["defaultRoot"])
        self.ui.actionSet_default_path.triggered.connect(self.__setDefaultRoot)
        self.ui.pushButton.clicked.connect(self.__returnSelection)
        self.ui.actionOverwrite.toggled.connect(self.__overwriteState)
        self.ui.actionShow_Valiadtion.toggled.connect(self.__validationState)
        #set column width
        self.ui.tV_file.setColumnWidth(0,260)
        self.ui.tV_file.setColumnWidth(1,60)
        self.ui.tV_file.setColumnWidth(2,80)
        self.ui.tV_file.setColumnWidth(3,100)

    def __overwriteState(self):
        self.__overwriteExist = self.ui.actionOverwrite.isChecked()
        #print self.__overwriteExist
    def __validationState(self):
        self.__showValidation= self.ui.actionShow_Valiadtion.isChecked()
        #print self.__showValidation

    def __setRootPath(self, rootpath):
        self.__model = QtGui.QFileSystemModel()
        self.__model.setNameFilters(["*.ma", "*.mb"])
        self.__model.setNameFilterDisables(False)
        path = QtCore.QDir(rootpath)
        self.__model.setRootPath(path.path())
        self.ui.tV_file.setModel(self.__model)
        self.ui.tV_file.setRootIndex(self.__model.index(path.path()))
        self.__seleciton = QtGui.QItemSelectionModel(self.__model)

    def __returnSelection(self):
        self.__tarFiles = []
        idx = self.ui.tV_file.selectedIndexes()
        if len(idx):
            for id in idx:
                if id.column() == 0:
                    data = self.ui.tV_file.model().filePath(id)
                    if os.path.isdir(data):
                        result = self.__recursiveFilesFinder(data)
                        if result:
                            self.__tarFiles += result
                    else:
                        self.__tarFiles.append(data)
        else:
            result = self.__recursiveFilesFinder(self.__usrConfig["defaultRoot"])        
            if result:
                self.__tarFiles += result
        if self.__tarFiles:
            self.__tarFiles = list(set(self.__tarFiles))
            self.__fileNameValidation()
        if self.__showValidation:
            self.__validationWindows()
        else:
            self.__smedgeSubmit()

    def __validationWindows(self):
        self.__validationList = QtGui.QWidget(self, QtCore.Qt.Popup | QtCore.Qt.Dialog)
        self.__validationList.setWindowModality(QtCore.Qt.WindowModal)
        self.uiValidation = validationUI.Ui_Form()
        self.uiValidation.setupUi(self.__validationList)
        itemModel =QtGui.QStandardItemModel()
        
        count = 0
        for i in self.__tarFileValidate.keys():
            item = QtGui.QStandardItem(i)
            itemModel.setItem(count, item)
            count += 1

        self.uiValidation.listView.setModel(itemModel)

        if self.__errFileName:  
            self.uiValidation.textEdit.append('---Error File Name Format----')
            for i in self.__errFileName:            
                self.uiValidation.textEdit.append(i)
            self.uiValidation.textEdit.append('')

        if self.__errExtension: 
            self.uiValidation.textEdit.append('---Error File Extension----')
            for i in self.__errExtension:            
                self.uiValidation.textEdit.append(i)
            self.uiValidation.textEdit.append('')

        if self.__errVersionFormat:
            self.uiValidation.textEdit.append('---Error File Version Format----')
            for i in self.__errVersionFormat:            
                self.uiValidation.textEdit.append(i)
            self.uiValidation.textEdit.append('')

        if self.__errTaskName:
            self.uiValidation.textEdit.append('---Error found no match task----')
            for i in self.__errTaskName:            
                self.uiValidation.textEdit.append(i)
            self.uiValidation.textEdit.append('')

        if self.__errFilePathInvalid:
            self.uiValidation.textEdit.append('---Error Target File Path not Existed----')
            for i in self.__errFilePathInvalid:            
                self.uiValidation.textEdit.append(i)
                
            self.uiValidation.textEdit.append('---Error Target File Path not Existed----')
            self.uiValidation.textEdit.append('')

        if self.__tarFileExist and not self.__overwriteExist:
            self.uiValidation.textEdit.append('---Error Target File already Existed----')
            for i in self.__tarFileExist:            
                self.uiValidation.textEdit.append(i)
            self.uiValidation.textEdit.append('')
        
        self.uiValidation.pushButton.setText("Submit (%d/%d)"%(len(self.__tarFileValidate), len(self.__tarFiles)))
        self.uiValidation.pushButton.clicked.connect(self.__smedgeSubmit)
        self.__validationList.setWindowTitle("CFX_Automation File Validation")      
        self.__validationList.show()

    def __recursiveFilesFinder(self, path):
        matches = []
        for root, dirnames, filenames in os.walk(path):
            for filename in filenames:    
                if filename.endswith('.ma') or filename.endswith('.mb'):
                    matches.append(os.path.join(root, filename))
        return matches

    def __genDefault(self):
        try: 
            os.makedirs(self.__usrDataPath)
        except OSError:
            if not os.path.isdir(self.__usrDataPath):
                raise

    def __setDefaultRoot(self):
        path = QtGui.QFileDialog.getExistingDirectory(self, 'Set', self.__usrConfig["defaultRoot"])
        if path:
            self.__setRootPath(path)
            self.__usrConfig["defaultRoot"] = path
            self.ui.lineEdit.setText(self.__usrConfig["defaultRoot"])
            self.__genConfig()

    def __fileNameValidation(self):
        self.__errFileName = []
        self.__errExtension = []
        self.__errVersionFormat = []
        self.__errFilePathInvalid = []
        self.__errTaskName = []
        self.__tarFileExist = []
        self.__validFilePath = []

        self.__tarFileValidate = {}
        for i in self.__tarFiles:
            i = os.path.abspath(i)
            episode = None
            fileBaseName = os.path.basename(i)
            fileData = fileBaseName.split('_')
            filePath = os.path.dirname(i)

            if len(fileData ) == 4:
                # check for episode
                epCheck = fileData[0].split('ep')
                if len(epCheck) == 2:
                    if len(epCheck[1]) == 2:
                        if epCheck[1].isdigit():
                            episode = fileData[0]
                            fileData.pop(0)

            if not len(fileData) == 3:
                self.__errFileName.append(i)
                #print 'err File name %s'%i
                #self.__tarFiles.remove(i)
            else:
                if not fileData[-1].endswith('.ma'):
                    self.__errExtension.append(i)
                    #print 'err File extension %s'%i
                    #self.__tarFiles.remove(i)
                version = fileData[-1].split('.')[0]
                #print version
                if not len(version) == 3:
                    self.__errVersionFormat.append(i)
                    #print 'err File version format, A %s'%i
                    #self.__tarFiles.remove(i)
                else:
                    versionPadding = version.split('v')
                    if not len(versionPadding) == 2:
                        self.__errVersionFormat.append(i)
                        #print 'err File version format, B %s'%i
                        #self.__tarFiles.remove(i)
                    else:
                        if not version[1].isdigit():
                            self.__errVersionFormat.append(i)
                            #print 'err File version format, C %s'%i
                            #self.__tarFiles.remove(i)
                        else:
                            self.__validFilePath.append(i)
                            '''
                            tarFilePath = self.__formFilePath(fileBaseName, episode)
                            tarFolder =  os.path.join(tarFilePath[0], tarFilePath[1])
                            if not os.path.isdir(tarFolder):
                                self.__errFilePathInvalid.append(i)
                                #print 'err tar folder path %s'%tarFilePath[0]
                                #self.__tarFiles.remove(i)
                            else:
                                tarFile = os.path.join(tarFolder , tarFilePath[2])
                                if os.path.isfile(tarFile):
                                    #print 'err File path %s'%tarFile
                                    if not self.__overwriteExist:
                                        self.__tarFileExist.append(i)
                                        #self.__tarFiles.remove(i)
                                    else:
                                        self.__tarFileValidate[i] = tarFilePath
                                else:
                                    self.__tarFileValidate[i] = tarFilePath
                            '''
        
        shotgunData = self.__getShotgunInfo(self.__validFilePath)
        for k in self.__validFilePath:
            fileBaseName = os.path.basename(k)
            fileNameData = fileBaseName.split('_')
            key = '_'.join(fileNameData[:2])
            if key in shotgunData.keys():
                if not 'errAnmPath' in shotgunData[key].keys():
                    tarFolder = shotgunData[key]['anmPath']
                    toWorkFolder = os.path.join(tarFolder, 'work')
                    toMayaWorkFolder = os.path.join(toWorkFolder , 'maya')
                    tarFilePath =  os.path.join(toMayaWorkFolder, '_'.join([fileNameData[1], fileNameData[2]]))
                    #print tarFilePath
                    if os.path.isfile(tarFilePath):
                        if not self.__overwriteExist:
                            self.__tarFileExist.append(k)
                        else:
                            self.__tarFileValidate[k] = tarFolder
                    else:
                        self.__tarFileValidate[k] = tarFolder
                else:
                    # file path not exited
                    self.__errFilePathInvalid.append(k)
                    #pass
            else:
                #err can't find task, so file path not existed
                self.__errTaskName.append(k)
                #pass

    def __getShotgunInfo(self, fileList):
        shotCode = []
        taskName = []
        for k in fileList:
            fileBaseName = os.path.basename(k)
            fileNameData = fileBaseName.split('_')
            shotCode.append(fileNameData[0])
            taskName.append(fileNameData[1])

        result = CFX_shotgunShotInfo.shotgunShotInfo(shotCode, taskName)
        if result:
            return result
        else:
            return False

        print result

    def __formFilePath(self, filename, episode=None):
        #toSeq = 'sequences'
        toSeq = os.path.join(projName, 'sequences')
        fileData =  os.path.basename(filename).split('_')
        shotNum = fileData[0][-4:]                    
        seqName = fileData[0][:-4]
        seqFolder = seqName
        if episode:
            shotNum = fileData[1][-4:]
            seqName = fileData[1][:-4]
            seqFolder = '_'.join([episode, seqName])

        tarfileName = '_'.join(fileData[-2:])
        toTarSeq = os.path.join(toSeq, seqFolder)
        shotFolder = seqName+shotNum
        toShotFolder = os.path.join(toTarSeq, shotFolder)
        toTaskName = os.path.join(toShotFolder, projConfig['project']['anm'])
        toWorkFolder = os.path.join(toTaskName, 'work')
        toMayaWorkFolder = os.path.join(toWorkFolder , 'maya')

        return [projRoot, toMayaWorkFolder, tarfileName]
      
        #return [projRoot, projName, toMayaWorkFolder, tarfileName]
      
    def __smedgeSubmit(self):
        pwd = os.path.abspath(__file__)
        pythonScript = os.path.join(pwd, os.path.join(projConfig['action']['path'],projConfig['action']['script']))
        
        for i in self.__tarFileValidate.keys():
            sjTemplate = CFX_utils.getConfig('sj')
            sjTemplate['Scene'] = i
            sjTemplate['name'] = os.path.basename(i)
            sjTemplate['PyScriptPath']

            sjFileName =  '.'.join(os.path.basename(i).split('.')[:-1])
            sjFile = os.path.join(self.__usrDataPath, (sjFileName+'.sj'))
            f = open( sjFile, 'w')
            f.write('[0]')
            f.write('\n')
            f.write('[00000000-0000-0000-0000-000000000001]')
            f.write('\n')
            for i in sjTemplate:
                f.write('%s=%s'%(i,sjTemplate[i]))
                f.write('\n')
            #print sjTemplate
            f.close()
            self.__validationList.close()

    def __genConfig(self):
        cfgfile = os.path.abspath(self.__usrConfigPath)
        with open( cfgfile, 'w') as f:
            json.dump(self.__usrConfig,f)

    def __loadConfig(self):
        cfgfile = os.path.abspath(self.__usrConfigPath)
        f = open(cfgfile)
        self.__usrConfig = json.load(f)
        f.close()

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = CFX_SubmitTool()
    mainWin.show()
    ret = app.exec_()
    sys.exit(ret)