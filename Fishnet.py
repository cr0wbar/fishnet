from FishnetUi import Ui_FishnetMainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from ProviderManager import ProviderManager
from sys import exit
from ProviderManagerDialog import ProviderManagerDialog
from Settings import Settings
from Engine import Engine
from QueryThread import QueryThread
from TorrentList import TorrentListModel, TorrentListView
from SettingsDialog import SettingsDialog
from StatusBarEventInterface import StatusBarEventInterface
import gc
from Startup import SplashScreen, StartupThread
from Globals import Globals
    
class Fishnet(Ui_FishnetMainWindow):

    class __FishnetAction(QtWidgets.QAction):
        
        chosen = QtCore.pyqtSignal(str)
        
        def __init__(self,text,parent):
            QtWidgets.QAction.__init__(self,text,parent)
            self.triggered.connect(self.__chosenWrapper)
            
        def __chosenWrapper(self):
            self.chosen.emit(self.text())

    def addItemToToolbar(self,iconpath,name,longDescr,methodToCall):
        toolbarItem = QtWidgets.QAction(QtGui.QIcon(iconpath),longDescr,self.parent)
        toolbarItem.setIconText(name)
        toolbarItem.triggered.connect(methodToCall)
        self.toolBar.addAction(toolbarItem)
        
    def copyMagnetlToClipboard(self):
        self.copyToClipboard("magnet")
        
    def copyToClipboard(self,key):
        data = self.getSelectedData()
        if data and key in data:
                provider = ProviderManager().instance.providers[data["provider"]]
                #If the link is in the page where the url points to, go get and fetch it
                opKey = key + "s"
                if "crawler" in provider["ops"][opKey]:
                    link = Engine().crawl(provider["baseUrl"], data[key], provider["ops"][opKey]["crawler"], provider["headers"] if "headers" in provider else None)
                #Otherwise just pass the stored link
                else:
                    link = data[key]
                #Copy the link to the clipboard (obtained statically)
                clipboard = QtWidgets.QApplication.clipboard()
                clipboard.setText(link)
    
    def clear(self):
        self.searchTextBox.clear()
        for _ in range(self.tabsWidget.count()):
            self.deleteTab()
        #Run the garbage collector
        gc.collect()
         
    def copyUrlToClipboard(self):
        self.copyToClipboard("url")
                
    def deleteTab(self):
        #We need to clear all the stuff contained in the tab, first we fetch the Q*view widget
        widget = self.tabsWidget.currentWidget()
        #Delete tab (doesn't free memory)
        self.tabsWidget.removeTab(self.tabsWidget.currentIndex())
        #Should free memory now
        if widget:
            widget.close()
            widget.deleteLater()
            widget.model().removeColumns(0,5)
            widget.model().deleteLater()
            widget.setParent(None)
            del widget        
        
    def exit(self,code):
        if QtCore.QThreadPool.globalInstance().activeThreadCount() > 0:
            self.showInfo("Wait for current operation to finish")
            return
        Settings().instance.getSettings()["defaultProvider"] = self.providerBox.text()
        Settings().instance.writeConfiguration(Globals.configurationPath)
        self.application.exit(code)
        
    def foo(self):
        print("FOO was called")
          
    def getSelectedData(self):
        torrentList  = self.tabsWidget.currentWidget()      
        if torrentList:
            selectedIndexes = torrentList.selectedIndexes()
            if selectedIndexes:
                #This is kind of a dirty trick, which exploits 
                #passing a tuple to the constructor of a QVariant.
                #Though it isn't quite beautiful, it works alright.
                for index in selectedIndexes:
                    data = torrentList.model().itemFromIndex(index).data()
                    if data:
                        return data[0]
        return None
    
    def prepareNewTab(self,tabText):
        model = TorrentListModel()
        
        torrentList = TorrentListView(self.tabsWidget)
        torrentList.setModel(model)
        torrentList.selectionModel().selectionChanged.connect(self.refreshClipboardMenu)
        
        self.tabsWidget.addTab(torrentList,tabText) #Add new tab
        self.tabsWidget.setCurrentWidget(torrentList) #Select new tab

        return model
                    
    def quit(self):
        self.exit(0)
                            
    def refreshClipboardMenu(self):
        data = self.getSelectedData()
        self.clipboardButton.menu().clear()
        if data:
            self.clipboardButton.setEnabled(True)
            if "magnet" in data:
                self.clipboardButton.menu().addAction(self.copyMagnetlToClipboardAction)
            if "url" in data:
                self.clipboardButton.menu().addAction(self.copyUrlToClipboardAction)
        else:
            self.clipboardButton.setEnabled(False)
            
    def reloadCategories(self):
        #The selected provider changed, we have to reload the categories in the box
        
        menu  = self.searchButton.menu()
        if not menu:
            self.searchButton.setMenu(QtWidgets.QMenu(self.searchButton))
            menu = self.searchButton.menu()
        else:
            menu.clear()
        
        cats = ProviderManager().instance.providers[self.providerBox.text()]["categories"]
        for cat in sorted(cats,key=cats.get):
            action = Fishnet.__FishnetAction(cat,parent=menu)
            action.chosen.connect(self.searchActionChosen)
            menu.addAction(action)
              
    def search(self,text,category,providerName):
        
        if providerName not in ProviderManager().instance.providers:
            self.showInfo("Please, select a valid provider.")
            return
        
        model = self.prepareNewTab(text+" ("+providerName+")") #Add new tab
        #Fetch data by using proxy function to Engine
        self.statusBarEventInterface.addOperation(Settings().instance.getSettings()["pages"])
        pool = QtCore.QThreadPool.globalInstance()
        query = QueryThread(text,category,Settings().instance.getSettings()["pages"],providerName)
        query.connector.newDataArrived.connect(model.update)
        query.connector.pageDone.connect(self.statusBarEventInterface.updateOperation)
        query.connector.finished.connect(self.statusBarEventInterface.finishedOperation)
        query.connector.Error.connect(self.showError)
        pool.start(query)
        
    @QtCore.pyqtSlot(str) 
    def searchActionChosen(self,category):
        self.search(self.searchTextBox.text(), category, self.providerBox.text())
        
    def searchAllUsingSelectedProvider(self):
        self.search(self.searchTextBox.text(),"All",self.providerBox.text())

    def searchAllInSingleTab(self):
        pool = QtCore.QThreadPool.globalInstance()
        text = self.searchTextBox.text()
        model = self.prepareNewTab(text+" (Aggregated)") #Add new tab  
        pages = Settings().instance.getSettings()["pages"]
        for providerName in ProviderManager().instance.providers.keys():
            self.statusBarEventInterface.addOperation(pages)
            query = QueryThread(text,"All",pages,providerName)
            query.connector.newDataArrived.connect(model.update)
            query.connector.pageDone.connect(self.statusBarEventInterface.updateOperation)
            query.connector.finished.connect(self.statusBarEventInterface.finishedOperation)
            query.connector.Error.connect(self.showError)
            pool.start(query)
            
                   
    def searchAllInMultipleTabs(self):
        text = self.searchTextBox.text()
        for providerName in ProviderManager().instance.providers.keys():
            self.search(text,"All", providerName)
    
    @QtCore.pyqtSlot(str)    
    def selectProvider(self,providerName):
        self.providerBox.setText(providerName)
        self.searchButton.setEnabled(True)
        self.reloadCategories()
        
    def setupShortCuts(self):
        self.defaultActionOnEnterKey = QtWidgets.QShortcut(QtCore.Qt.Key_Return,self.searchTextBox,self.searchAllUsingSelectedProvider)
        
    def setupSignals(self):
        self.searchButton.clicked.connect(self.searchAllUsingSelectedProvider)
        self.clearAllButton.clicked.connect(self.clear)
        self.actionQuit.triggered.connect(self.quit)
        self.actionManage_providers.triggered.connect(self.showProviderManagerUi)
        self.actionAbout.triggered.connect(self.showAbout)
        self.tabsWidget.currentChanged.connect(self.refreshClipboardMenu)
        self.copyUrlToClipboardAction.triggered.connect(self.copyUrlToClipboard)
        self.copyMagnetlToClipboardAction.triggered.connect(self.copyMagnetlToClipboard)
        self.actionEdit_settings.triggered.connect(self.showSettings)
        ProviderManager().instance.sendError.connect(self.showError)
        Settings().instance.sendError.connect(self.showError)

    def setupUi(self,MainWindow,Application):
        
        #Load Application and Main Window
        self.parent = MainWindow
        self.application = Application 
        
        #Set nice look for our beloved MacOs users
        self.parent.setUnifiedTitleAndToolBarOnMac(True)
        
        #SuperClass UI setup
        Ui_FishnetMainWindow.setupUi(self,self.parent)

        #Get application path
        _root = Globals().rootPath()
        #Load Icons
        self.searchIcon = QtGui.QIcon(_root+"icons/search.png")
        self.addIcon = QtGui.QIcon(_root+"icons/add.png")
        self.searchAllIcon = QtGui.QIcon(_root+"icons/search-all.png")
        self.removeIcon =  QtGui.QIcon(_root+"icons/remove.png")
        self.removeAllIcon = QtGui.QIcon(_root+"icons/remove-all.png")

        #Set the icons of the buttons
        self.searchButton.setIcon(self.searchIcon)
        self.searchAllButton.setIcon(self.searchAllIcon)
        self.clearAllButton.setIcon(self.removeAllIcon)

        #Set option for Search ALl button
        searchAllInSingleTabAction = QtWidgets.QAction("Single tab",self.parent)
        searchAllInSingleTabAction.triggered.connect(self.searchAllInSingleTab)
        searchAllInMultipleTabsAction = QtWidgets.QAction("Multiple tabs",self.parent)
        searchAllInMultipleTabsAction.triggered.connect(self.searchAllInMultipleTabs)
        self.searchAllButton.addActions([searchAllInMultipleTabsAction,searchAllInSingleTabAction])
        
        #Setup toolbar
        #First set the clipboard button, which contains a menu
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.clipboardButton = QtWidgets.QToolButton()
        self.clipboardButton.setText("Copy")
        self.clipboardButton.setAutoRaise(True)
        self.clipboardButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.clipboardButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.clipboardButton.setIcon(QtGui.QIcon(_root+"icons/clipboard.png"))
        self.clipboardButton.setMenu(QtWidgets.QMenu(self.clipboardButton))#Create menu for popup
        
        #Then create the possible actions
        self.copyMagnetlToClipboardAction = QtWidgets.QAction("magnet to clipboard",self.parent)
        self.copyUrlToClipboardAction = QtWidgets.QAction("URL to clipboard",self.parent)
        self.clipboardButton.setEnabled(False)#Disabled at startup
        self.toolBar.addWidget(self.clipboardButton)
        
        #Add other buttons to toolbar
        #self.addItemToToolbar(_root+"icons/send.png", "Send","Send torrent to external application",self.foo)
        self.toolBar.addSeparator()
        self.addItemToToolbar(_root+"icons/settings.png", "Settings","Open settings page", self.showSettings)
        self.addItemToToolbar(_root+"icons/configure-providers.png", "Providers","Manage providers", self.showProviderManagerUi)
        self.toolBar.addSeparator()
        self.addItemToToolbar(_root+"icons/about.png", "About","About F1s#n3t", self.showAbout)
        self.addItemToToolbar(_root+"icons/leave.png", "Leave","Leave F1s#n3t",self.quit)#Quit   

        #Options for tabsWidget
        self.tabsWidget.tabCloseRequested.connect(self.deleteTab)
        self.tabsWidget.setTabsClosable(True)
        
        #Misc
        self.statusBarEventInterface = StatusBarEventInterface(self.statusbar)
        
        #Connect GUI elements to actions
        self.setupSignals()
        
        #Setup shortcuts
        self.setupShortCuts()
        
    def showAbout(self):
        QtWidgets.QMessageBox.about(QtWidgets.QWidget(self.parent),"About F1s#n3t","<b><font face=\"courier new\" size=25>F1s#n3t</font></b><br/>\
                                                                <b>Version: </b>"+Globals.version+"<br/>\
                                                                <b>Author: </b>Guglielmo De Concini &lt;" + Globals.mailTo+"&gt;")
           
    def showProviderManagerUi(self):
        diag = QtWidgets.QDialog(self.parent)
        pmd = ProviderManagerDialog()
        pmd.setupUi(diag)
        diag.exec_()
        if pmd.save:
            msg = "In order to apply the changes F1s#n3t has to restart.<br/>Do you want to restart now?"
            box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,"Information",msg,buttons=QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            if box.exec_() == QtWidgets.QMessageBox.Ok:
                self.exit(1705)
        
    def showInfo(self,msg):
        box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,"Information",msg)
        box.exec_()
        
    @QtCore.pyqtSlot(str)
    def showError(self,msg):
        reportABug = "<br/><b>Now what? </b>Contact the developer and tell him this software sucks,"\
                     "or kindly <a href=\""+Globals.reportABugLink+"\">report a bug</a> (if you think this is a bug), whatever!"
        box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,"Error","<b>Error:</b> "+msg + reportABug)
        box.exec_()
    
    def showSettings(self):
        diag = QtWidgets.QDialog(self.parent)
        sd = SettingsDialog()
        sd.setupUi(diag)
        diag.exec_()
        
    def startup(self):
        #Hide main window
        self.parent.hide()
        self.splashScreen = SplashScreen(self.application)

        #Setup the thread that will load the
        self.startupThread = StartupThread()
        self.startupThread.finished.connect(self.startupFinished)   

        #Connect signals
        self.startupThread.started.connect(self.splashScreen.startProgress)
        self.startupThread.finished.connect(self.splashScreen.finish)
        Settings().instance.providerLoading.connect(self.splashScreen.updateProgress)
        
        self.startupThread.start()

    def startupFinished(self):
        #Delete startup thread
        self.splashScreen.deleteLater()
        self.startupThread.deleteLater()

        self.parent.show()
        
        providers = ProviderManager().instance.providers
        
        menu = self.providerBox.menu()
        if menu:
            menu.clear()
        else:
            menu = QtWidgets.QMenu(self.providerBox)  
            self.providerBox.setMenu(menu)
            
        if providers:
            #Add an option in the button's menu for each provider's name
            for providerName in providers:
                action = Fishnet.__FishnetAction(providerName,parent=self.providerBox)
                action.chosen.connect(self.selectProvider)
                menu.addAction(action)       
            
            #Set default provider (if any)
            settings = Settings().instance.getSettings()
            if "defaultProvider" in settings:
                defaultProvider = settings["defaultProvider"]

                if defaultProvider in providers:
                    self.selectProvider(defaultProvider)
                    return
        
        self.searchButton.setDisabled(True)
        self.providerBox.setText("Select provider")
        
if __name__ == "__main__":
    import sys

    ret = 1705
    a = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()
    ui = Fishnet()
    ui.setupUi(w, a)

    while ret == 1705:
        ui.startup()
        ret = a.exec_()
        
    exit(ret)

