from PyQt5 import QtCore, QtWidgets
class StatusBarEventInterface:
    
    def __init__(self,statusBar):
        self.statusBar = statusBar
        self.progressBar = QtWidgets.QProgressBar(self.statusBar)
        self.statusBar.addPermanentWidget(self.progressBar)

        self.__reset()
        
    def addOperation(self,steps):
        self.steps += steps
        if self.progressBar.isHidden():
            self.progressBar.show()

    def updateOperation(self):
        self.iterations+=1
        self.progressBar.setValue(int(100.*float(self.iterations)/float(self.steps)))    
        
    @QtCore.pyqtSlot(int)
    def finishedOperation(self,stepsLeft):
        
        if stepsLeft > 0 :
            self.iterations+=stepsLeft
            self.progressBar.setValue(int(100.*float(self.iterations)/float(self.steps))) 
        if self.iterations == self.steps:    
            self.__reset()
            
    def __reset(self):
        if not self.progressBar.isHidden():
            self.progressBar.hide()
            self.progressBar.setValue(0)
            self.statusBar.showMessage("All operations completed",2000)
        self.steps = 0
        self.iterations = 0