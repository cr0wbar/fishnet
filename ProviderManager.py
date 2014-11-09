import json
from Engine import Engine
from urllib3 import PoolManager,Timeout
from PyQt5 import QtCore

class ProviderManager:
     
    class __ProviderManager(QtCore.QObject):
        
        sendError = QtCore.pyqtSignal(str)
        
        def __init__(self):
            QtCore.QObject.__init__(self)
            self.providers = {}
            self.poolManager = PoolManager(timeout=Timeout(10),
                                           headers={'Accept-Encoding': 'gzip,deflate'})
            self.engine = Engine()
        
        def loadProviderFromFile(self,path):
            try:
                providerFile = open(path,mode="r")
                provider = json.loads(providerFile.read())
                providerFile.close()
                self.providers[provider["name"]] = provider
            except Exception as e:
                self.sendError.emit("cannot load provider at '"+path+"' <br/><b>Reason:</b> "+str(e))
                
        def loadProviderFromUrl(self,url):
            try:
                req = self.poolManager.request("GET", url)
                provider = json.loads(req.data.decode('utf-8'))
                self.providers[provider["name"]] = provider
                del req
            except Exception as e:
                self.sendError.emit("cannot load provider at '"+url+"' <br/><b>Reason:</b> "+str(e))
                
        def queryProvider(self,text,category,pages,providerName,perPageCallback=None,whenDoneCallback=None):#Exceptions here should be managed by the caller
            return self.engine.makeQuery(self.providers[providerName], text, category, pages,perPageCallback,whenDoneCallback)
        
        def reset(self):
            if  self.providers:
                self.providers.clear() 
                
    instance = None
        
    def __init__(self):
        if not self.instance:
            ProviderManager.instance = ProviderManager.__ProviderManager()
    

            