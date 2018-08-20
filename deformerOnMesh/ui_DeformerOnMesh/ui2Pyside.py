import os, sys, pprint
from pysideuic import compileUi
from PySide import QtCore, QtGui

class ui2Pyside(QtGui.QWidget):
    #'convert qt designer ui to py'
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.path, _ = QtGui.QFileDialog.getOpenFileNames(self, "Open File", os.getcwd(),"UI files (*.ui)")
        if self.path:
            for i in self.path:
                self.writePy(i)
        self.exitUI()
        
    def writePy(self,path):
        tarFile = '.'.join(path.split('.')[0:-1])+'.py'
        try:
            pyfile = open(tarFile, 'w')
            compileUi(path, pyfile, False, 4, False)
            pyfile.close()
            print('Sucessfully convert %s to %s'%(path,tarFile))
        except:
            print('failed to convert %s'%path)
                
    def exitUI(self):
        self.deleteLater()
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = ui2Pyside()
    window.show()
    sys.exit(app.exec_())
