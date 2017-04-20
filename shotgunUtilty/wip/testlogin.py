from PySide.QtCore import *
from PySide.QtGui import *
import sys,os,glob,platform,datetime,urllib

class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent,Qt.FramelessWindowHint)
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)
        self.textPass.setEchoMode(QLineEdit.Password);
        
    def handleLogin(self):
        if (self.textName.text() != '' and
            self.textPass.text() != ''):
            self.accept()
        else:
            QMessageBox.warning(
                self, 'Error', "usrname and passwd can't be empty")
    
    def returnLoginData(self):
        return [self.textName.text(),self.textPass.text()]

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        login = Login(self)

        if login.exec_() == QDialog.Accepted:
            print login.returnLoginData()
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)    

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)

    window = Window()
    window.show()
    sys.exit(app.exec_())

