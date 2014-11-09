from os.path import expanduser
from PyQt5 import QtCore

'''
Until pyqtdeploy guys implement a way
to check if an application is bundled 
or not, we will use this horrible way 
of knowing where we are. When 
'''
'''
try import pyqtdeploy:
    import sys
    rootPath = QtCore.QFileInfo(sys.executable).absolutePath() + "/"
except ImportError:
    rootPath = QtCore.QFileInfo(__file__).absolutePath() + "/"
'''


class Globals:
    
    __rootPath = None
    configurationPath = expanduser("~")+"/"+".fishnet"
    reportABugLink = "https://github.com/cr0wbar/fishnet/issues"
    programDescription = "A simple tool to search for torrents."
    mailTo = "guglielmo.deconcini@gmail.com"
    version = "0.9-SNAPSHOT"
    
    def __init__(self):
        if not self.__rootPath:
            try :
                from sys import frozen,executable
                Globals.__rootPath = QtCore.QFileInfo(executable).absolutePath() + "/"
            except ImportError:
                Globals.__rootPath = QtCore.QFileInfo(__file__).absolutePath() + "/"
        
    def rootPath(self):
        '''
        If the application is deployed, frozen is set.
        In the following code the application gets the right path for resources
        '''
        return Globals.__rootPath
    