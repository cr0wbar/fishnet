from PyQt5 import QtCore

from json import loads,dumps
from urllib3 import PoolManager,Timeout
from ProviderManager import ProviderManager
from os.path import isfile
from Globals import Globals

class Settings:
    
    class __Settings(QtCore.QObject):
        
        sendError = QtCore.pyqtSignal(str)
        providerLoading = QtCore.pyqtSignal(int,str)
        
        def __init__(self):
            QtCore.QObject.__init__(self)
            
            self.__pm = PoolManager(timeout=Timeout(10),
                                    headers={'Accept-Encoding': 'gzip,deflate'})
            self.__settings = None
            self.providersListDefaultValue = "https://raw.githubusercontent.com/cr0wbar/fishnet/master/providers.json"
            self.downloadProvidersListAtStartupDefaultValue = True
            self.providersDefaultValue = {"remote":[],"local":[]}
            self.pagesDefaultValue = 3
        
        def __checkSettingsSanity(self):
            if not self.__settings:
                self.__settings = {}
            if not "downloadProvidersListAtStartup" in self.__settings:
                self.__settings["downloadProvidersListAtStartup"] = self.downloadProvidersListAtStartupDefaultValue
            if not "providersList" in self.__settings:
                self.__settings["providersList"] = self.providersListDefaultValue
            if not "providers" in self.__settings:
                self.__settings["providers"] = self.providersDefaultValue
            if not "pages" in self.__settings:
                self.__settings["pages"] = self.pagesDefaultValue              
            
        def getSettings(self):
            return self.__settings
        
        def loadConfiguration(self,path):
            if not isfile(path):
                self.__checkSettingsSanity()
            else:
                
                try:
                    sfile = open(path,"r")
                    self.__settings = loads(sfile.read())
                    sfile.close()
                except IOError as e:
                    self.sendError.emit("Cannot open configuration at '"+path+"' <br/><b>Reason:<b/>" + str(e))
                finally:
                    self.__checkSettingsSanity()

        
        def loadProviders(self):
            #Check if there is a url for the list of providers
            #If there is and we are supposed to download the list,
            #then proceed to download the list.
            #Then download each provider in the downloaded list
            providerManager = ProviderManager().instance
              
            providerManager.reset()
            
            if self.__settings and "downloadProvidersListAtStartup" in self.__settings and self.__settings["downloadProvidersListAtStartup"]:
                
                try:#Load remote list of providers
                    r = self.__pm.urlopen("GET", self.__settings["providersList"])
                    self.providerLoading.emit(10,"Loading list of providers")
                    providersList = loads(r.data.decode("utf-8"))
                    if "list" in providersList:
                        self.__settings["providers"]["remote"].clear()
                        for providerUrl in providersList["list"]:
                            self.__settings["providers"]["remote"].append(providerUrl)
                            
                except Exception as e:
                    self.sendError.emit("cannot retrieve the list of providers at '"+self.__settings["providersList"]+"'<br/><b>Reason:</b> "+str(e))       

            #Load stored remote providers
            
            totalNumberOfProviders = 0
            providersLoaded = 0
            
            if self.__settings and "remote" in self.__settings["providers"]:
                totalNumberOfProviders+=len(self.__settings["providers"]["remote"])
            if self.__settings and "local" in self.__settings["providers"]:
                totalNumberOfProviders+=len(self.__settings["providers"]["local"])
                    
            if self.__settings and "remote" in self.__settings["providers"]:
                for remoteProvider in self.__settings["providers"]["remote"]:
                    providersLoaded+=1
                    self.providerLoading.emit(int(10.+float(providersLoaded)/float(totalNumberOfProviders)*90.),
                                              "Loading provider at "+remoteProvider)
                    providerManager.loadProviderFromUrl(remoteProvider)
                         
            #Load stored local providers
            if self.__settings and "local" in self.__settings["providers"]:
                for localProvider in self.__settings["providers"]["local"]:
                    providersLoaded+=1
                    self.providerLoading.emit(int(10.+float(providersLoaded)/float(totalNumberOfProviders)*90.),
                                              "Loading provider at "+localProvider)
                    providerManager.loadProviderFromFile(localProvider)
                    
        def setDefaultProvider(self,provider):
            self.__settings["defaultProvider"] = provider
            
        def writeConfiguration(self,path):
            try:
                sfile = open(path,"w")
                sfile.write(dumps(self.__settings))
                sfile.close()
            except IOError as e:
                self.sendError.emit("cannot open configuration at '"+Globals.configurationPath+"'<br/><b>Reason:</b> " + str(e))

                
    instance = None
    
    def __init__(self):
        if not self.instance:
            Settings.instance = Settings.__Settings()