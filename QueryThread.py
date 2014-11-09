from ProviderManager import ProviderManager
from PyQt5 import QtCore
                        
class QueryThread(QtCore.QRunnable):
    
    class __Connector(QtCore.QObject):
        
        newDataArrived = QtCore.pyqtSignal(dict,str,int)
        pageDone = QtCore.pyqtSignal()
        finished = QtCore.pyqtSignal(int)
        Error = QtCore.pyqtSignal(str)
        
        def __init__(self,pagesToDo):
            QtCore.QObject.__init__(self)
            self.pagesDone = 0
            self.pagesToDo = pagesToDo
            
        def sendFinished(self):
            self.finished.emit(self.pagesToDo-self.pagesDone)
            
        def sendNewData(self,rawData,providerName,nitems):
            self.newDataArrived.emit(rawData,providerName,nitems)
            self.pagesDone+=1
            self.pageDone.emit()
            
        def sendError(self,err):
            self.Error.emit(err)
            
    def __init__(self,
                 text,# The text to search 
                 category,#The category
                 pages,#The number of pages to fetch 
                 providerName):#the name of the provider, 'name' in the configuration
        
        QtCore.QRunnable.__init__(self)
        self.setAutoDelete(True)

        self.text = text
        self.category = category
        self.pages = pages
        self.providerName = providerName
        self.connector = QueryThread.__Connector(self.pages)
        
    def run(self):
        try:
            ProviderManager().instance.queryProvider(self.text,
                                                     self.category,
                                                     self.pages,
                                                     self.providerName,
                                                     perPageCallback=self.connector.sendNewData,
                                                     whenDoneCallback=self.connector.sendFinished)
        except Exception as exc:
            self.connector.sendError("query '"+self.text+"' for provider '"+self.providerName+"' failed.<br/><b>Reason:</b> "+str(exc))
            self.connector.sendFinished()

        
