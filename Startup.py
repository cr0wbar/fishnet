from PyQt5 import QtCore,QtGui,QtWidgets
from Settings import Settings
from Globals import Globals

class SplashScreen(QtCore.QObject):
    
    def __init__(self,app):
        QtCore.QObject.__init__(self)
        _root = Globals().rootPath()
        #This allows icons to be loaded even after the application has been deployed
        self.splash = QtWidgets.QSplashScreen(QtGui.QPixmap(_root +"misc/splash.png"))
        self.app = app
        font = QtGui.QFont()
        font.setPixelSize(10)
        self.splash.setFont(font)
        self.progressBar = QtWidgets.QProgressBar(self.splash)
        self.progressBar.setGeometry(self.splash.width()*0.05, self.splash.height()*0.8,self.splash.width()*0.9, self.splash.height()*0.075)
        self.splash.rect = QtCore.QRect()
        self.textColor = QtGui.QColor("white")
        
    def startProgress(self):
        self.splash.show()
        self.app.processEvents()
        
    @QtCore.pyqtSlot(int,str)
    def updateProgress(self,progress,msg):
        self.splash.showMessage(msg,alignment = QtCore.Qt.AlignBottom,color=self.textColor)
        self.progressBar.setValue(progress)
        self.app.processEvents()
        
    def finish(self):
        self.progressBar.deleteLater()
        self.splash.deleteLater()
        
class StartupThread(QtCore.QThread):
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        settings = Settings().instance 
        settings.loadConfiguration(Globals.configurationPath)
        settings.loadProviders()
  
    