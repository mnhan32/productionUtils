import os,fnmatch,sys,datetime
from operator import itemgetter
from itertools import *
from PySide import QtCore, QtGui
import ui_missingFrameReport as UI


def missing_in_seq(*args):
    if len(args)==1:
        start=args[0][0]
        end=args[0][-1]
    else:
        start=args[1]
        end=args[2]
         
    return sorted(set(range(start,end+1)).difference(args[0]))

def missingFrameFormat(inputList):
    outList=[]
    for k, g in groupby(enumerate(inputList), lambda x:x[0]-x[1]):
        group = list(map(itemgetter(1), g))
        outList.append((group[0], group[-1]))
    return outList


def writeReport(mode,tar,extType,start,end):
    # if include all sub
    timeStamp=datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    if mode:
        f=open(os.path.join(tar,'missingFrameReport_%s.log'%timeStamp),'w')
        f.write('\n %s  \n'%timeStamp)
        f.write('\n Missing Frames Report, frame range %s - %s'%(start,end))
        
    for rootFolder in os.walk(tar): 
        imageSeq=[]
        for ext in extType:
            matchFiles=sorted(fnmatch.filter(rootFolder[2],"*.%s"%ext))
            switchPad=0
            if matchFiles:
                for m in matchFiles:
                    seqName='.'.join(m.split('.')[0:-2])
                    if seqName!='':
                        #imageSeq.append([seqName,m])
                        imageSeq.append(m)
                        if switchPad==0:
                            padding=len(list(m.split('.')[-2]))
                            switchPad=1
                        
                if imageSeq:
                    #print imageSeq
                    
                    print 'PATH : %s'%rootFolder[0]
                    print '----------'
                    
                    if mode:                        
                        f.write('\n\n--------------------------\n')
                        f.write('PATH : %s'%rootFolder[0])
                        f.write('\n--------------------------\n\n')
                    
                    for key,group in groupby(imageSeq, lambda x: '.'.join(x.split('.')[0:-2])):
                        if not padding:
                            padding =4
                        
                        print 'Seq Name : %s.%s.%s'%(key,'#'*padding,ext)
                        
                                            
                        serialNum=[]
                        for a in group:
                            #print a
                            serialNum.append(int(a.split('.')[-2]))
                        if serialNum:
                            missingFrames=missing_in_seq(serialNum,start,end)
                            fortmatMissingFrames=missingFrameFormat(missingFrames)
                            
                            print 'There are %s missing frames'%len(missingFrames)
                            if mode:
                                f.write('Seq Name : %s.%s.%s'%(key,'#'*padding,ext))
                                f.write(' (missing %s frames)\n'%len(missingFrames))
                                
                            if fortmatMissingFrames:
                                missingFrameStr=''
                                for idx, fr in enumerate(fortmatMissingFrames):
                                    if fr[0]!=fr[1]:
                                        missingFrameStr+='%s-%s'%(fr[0],fr[-1])
                                    else:
                                        missingFrameStr+='%s'%fr[0]

                                    if idx!=len(fortmatMissingFrames)-1:
                                        missingFrameStr+=','
                            else:
                                print '%s'%'There are no missing frames.'
                            
                            print missingFrameStr
                            print ''
                            if mode:
                                f.write(missingFrameStr)
                                f.write('\n\n')
                                
                print '--------'
              
            else:
                print '%s'%'no seq existed.'
    if mode:
        f.write('\n End of Missing Frames Report\n')
        f.close()



class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = UI.Ui_mainWindow()
        self.ui.setupUi(self)
        self.init()

    def init(self):
        self.ui.tB_dir.clicked.connect(self.openDirectoryDialog)
        self.ui.pB_run.clicked.connect(self.runIt)
        
    def openDirectoryDialog(self):
        flags = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self,"Open Directory",os.getcwd(),flags)
        self.ui.lE_dir.setText(directory)
    
    def runIt(self):
        start=self.ui.sB_start.value()
        end=self.ui.sB_end.value()
        tarPath=self.ui.lE_dir.text()
        extType=str(self.ui.lE_ext.text()).split(' ')
        print extType
        
        if os.path.isdir(tarPath):
            if start>0 and end >0 and end > start:
                if extType:
                    writeReport(1,tarPath,extType,start,end)
                else:
                    print '%s'%'extension type not defined.'
            else:
                print '%s'%'frame range format error'
        else:
            print '%s'%'target folder not existed.'
    
if __name__== '__main__':
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())
