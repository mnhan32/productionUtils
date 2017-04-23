from PySide import QtGui, QtCore
import os,sys,json


class taskWidget(QtGui.QWidget):
    
    #test
    _k = 'test'

    def __init__(self):
        super(taskWidget,self).__init__()
        self.tableView=QtGui.QTableView()
        self.tableView.setIconSize(QtCore.QSize(72,36))
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.doubleClicked.connect(self.selectTrigger)
        print '%s in init'%_k
        layout=QtGui.QVBoxLayout(self)
        layout.addWidget(self.tableView)
        self.setLayout(layout)

    def selectTrigger(self):
        idx = self.tableView.selectedIndexes()[0]
        userData = self.tableView.model().data(idx,QtCore.Qt.UserRole)
        print '%s in douvle clicked'%_k
        #print userData


if __name__ == '__main__':
    dirLoc = os.path.dirname(__file__)
    home = os.path.expanduser("~")
    folderName = '.wefxstudio.shotgunstudio.com'
    preference = os.path.join(home,folderName)
    #if not os.path.isdir(perference):
        #os.mkdir(preference)
    

    app = QtGui.QApplication(sys.argv)
    mainWin = taskWidget()
    dataModel = QtGui.QStandardItemModel()
    itemIcon = QtGui.QIcon()
    itemIcon.addPixmap('/T/productionPythonEnv/productionUtils/shotgunUtils/icon/unkonwn.png')
    itemA = QtGui.QStandardItem(itemIcon,'test')
    itemA.setData('ABC', QtCore.Qt.UserRole)
    dataModel.appendRow(itemA)
    mainWin.tableView.setModel(dataModel)
    mainWin.tableView.resizeRowsToContents()
    mainWin.tableView.resizeColumnsToContents()

    dataA = [{
                "Project":{
                            "id":1234,
                            "name":"MYS"
                    },
                "id":1513,
                "step":"dlvr"
                },
            {
                "Project":{
                            "id":451,
                            "name":"test"
                    },
                "id":513,
                "step":"ip"
                }
            ]
    jData = json.dumps(dataA)

    print jData
    iData = json.loads(jData)
    print iData
    print type(iData)
    
    #with open()
    mainWin.show()
    ret = app.exec_()
    sys.exit(ret)
