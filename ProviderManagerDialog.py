from ProviderManagerDialogUi import Ui_ProviderManagerDialog
from PyQt5 import QtGui,QtWidgets
from Settings import Settings 

class ProviderManagerDialog(Ui_ProviderManagerDialog):
    
    def __addLocalProvider(self):
        path,_ = QtWidgets.QFileDialog.getOpenFileName(parent=None,\
                                           caption='Open provider from file',\
                                           filter='*.json')
        if path:
            item = QtGui.QStandardItem(path)
            item.setIcon(self.localIcon)
            item.setEditable(False)
            self.providersList.model().appendRow(item)
            if "local" not in self.__providers:
                self.__providers["local"] = []
            self.__providers["local"].append(path)
            
    def __addRemoteProvider(self):
        url,accepted = QtWidgets.QInputDialog.getText(self.parent, "Add new remote provider", "Insert the provider's url",text="http://")
        if accepted:
            self.__providers["remote"].append(url)
            item = QtGui.QStandardItem(url)
            item.setIcon(self.remoteIcon)
            item.setEditable(False)
            self.providersList.model().appendRow(item)
            
    def __cancel(self):
        del self.__providers
        self.__clear()
        self.parent.close()
        
    def __clear(self):
        self.providersList.deleteLater()

    def __removeProvider(self):
        index = self.providersList.currentIndex()
        if index:
            model = self.providersList.model()
            item = model.itemFromIndex(index)
            if not item:
                return
            prov = item.text()
            model.removeRows(index.row(),1)
            if prov in self.__providers["remote"]:#Rather revolting
                self.__providers["remote"].remove(prov)
            else:
                self.__providers["local"].remove(prov)
    
    def __save(self):
        origProviders = Settings().instance.getSettings()["providers"]
        for key in ["local","remote"]:
            origProviders[key].clear()
            origProviders[key] = self.__providers[key]
        self.save = True
        self.__clear()
        self.parent.close()
    
    def __loadFromsettings(self):
        #Save providers for editing, copy them back if editing is accepted
        origProviders = Settings().instance.getSettings()["providers"]
        self.__providers = {"local":list(origProviders["local"]),"remote":list(origProviders["remote"])}#This is horrible :(
        
        model = QtGui.QStandardItemModel(self.providersList)
        if "local" in self.__providers:
            for p in self.__providers["local"]:
                item = QtGui.QStandardItem(p)
                item.setIcon(self.localIcon)
                item.setEditable(False)
                model.appendRow(item)
        if "remote" in self.__providers:
            for p in self.__providers["remote"]:
                item = QtGui.QStandardItem(p)
                item.setIcon(self.remoteIcon)
                item.setEditable(False)
                model.appendRow(item)
                
        self.providersList.setModel(model)
        
    def setupUi(self, Dialog):
        from Globals import Globals
        
        self.parent = Dialog
        super().setupUi(Dialog)
        
        #Get path
        _root = Globals().rootPath()
        #Setup ToolBUtton(s) icon(s)
        self.addNewProviderButton.setIcon(QtGui.QIcon(_root+"icons/add.png"))
        self.removeProviderButton.setIcon(QtGui.QIcon(_root+"icons/remove.png"))
        self.localIcon = QtGui.QIcon(_root+"icons/local.png")
        self.remoteIcon = QtGui.QIcon(_root+"icons/remote.png")
        #Extra setup of the manager's UI
        addMenu = QtWidgets.QMenu(Dialog)
        localAction = QtWidgets.QAction(self.localIcon,"Local",self.providersList)
        localAction.triggered.connect(self.__addLocalProvider)
        remoteAction = QtWidgets.QAction(self.remoteIcon,"Remote",self.providersList)
        remoteAction.triggered.connect(self.__addRemoteProvider)
        addMenu.addActions([localAction,remoteAction])
        self.addNewProviderButton.setMenu(addMenu)     
        self.removeProviderButton.clicked.connect(self.__removeProvider)
        self.buttonBox.accepted.connect(self.__save)
        self.buttonBox.rejected.connect(self.__cancel)
        self.__loadFromsettings()
        self.save = False