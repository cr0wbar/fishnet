from utils import deformatSize

from PyQt5 import QtCore, QtGui, QtWidgets

class TorrentListItem(QtGui.QStandardItem):
        
    def __init__(self,string):
        QtGui.QStandardItem.__init__(self,string)
        self.setEditable(False)   
     
class TorrentListSizeItem(TorrentListItem):
    
    def __init__(self,string):
        TorrentListItem.__init__(self, string)
        self.value = deformatSize(string)
        
    def __lt__(self, otherItem):
        return self.value > otherItem.value
    
class TorrentListNumericItem(TorrentListItem):
    
    def __init__(self,string):
        TorrentListItem.__init__(self, string)
        stripped = string.strip()
        self.value = int(stripped) if stripped.isdigit() else -1
        
    def __lt__(self, otherItem):
        return self.value > otherItem.value
    
class TorrentListModel(QtGui.QStandardItemModel):
    
    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)
        self.setHorizontalHeaderLabels(["Category","Name","Size","Seeders","Leechers"])
        
    @QtCore.pyqtSlot(dict,str,int)
    def update(self,rawData,providerName,nitems):   
        cols = []

        for op in ["categories","titles","sizes","seeders","leechers"]:
            if op in rawData:
                cols.append(rawData[op])
                del rawData[op]
            else:
                cols.append(["N/A" for _ in range(nitems)])
        
        #Even though the following code is not wrong, is quite redundant (and ugly), it should be simplified in some way..        
        if "urls" in rawData and "magnets" in rawData:
            for row,url,magnet in zip(zip(*cols),rawData["urls"],rawData["magnets"]):
                rowItems = [TorrentListItem(row[0]),
                            TorrentListItem(row[1]),
                            TorrentListSizeItem(row[2]),
                            TorrentListNumericItem(row[3]),
                            TorrentListNumericItem(row[4])]
                rowItems[0].setData( QtCore.QVariant(({"provider":providerName,"url":url,"magnet":magnet},)) )
                self.appendRow(rowItems)
            del rawData["urls"]
            del rawData["magnets"]
            del rawData
            
        elif "magnets" in rawData:
            for row,magnet in zip(zip(*cols),rawData["magnets"]):
                rowItems = [TorrentListItem(row[0]),
                            TorrentListItem(row[1]),
                            TorrentListSizeItem(row[2]),
                            TorrentListNumericItem(row[3]),
                            TorrentListNumericItem(row[4])]
                rowItems[0].setData( QtCore.QVariant(({"provider":providerName,"magnet":magnet},)) )
                self.appendRow(rowItems)
            del rawData["magnets"]
            del rawData
            
        else:
            for row,url in zip(zip(*cols),rawData["urls"]):
                rowItems = [TorrentListItem(row[0]),
                            TorrentListItem(row[1]),
                            TorrentListSizeItem(row[2]),
                            TorrentListNumericItem(row[3]),
                            TorrentListNumericItem(row[4])]
                rowItems[0].setData( QtCore.QVariant(({"provider":providerName,"url":url},)) )
                self.appendRow(rowItems)
            del rawData["urls"]
            del rawData
        
class TorrentListView(QtWidgets.QTreeView):
    
        def setModel(self,model): 
            QtWidgets.QTreeView.setModel(self,model)
              
            self.setColumnWidth(1,600) #Set the 'name' column larger
            self.setColumnWidth(3,50) #Set the 'seeders' column smaller
            self.setColumnWidth(4,50) #Set the 'leechers' column smaller
            
            self.setSortingEnabled(True) #Activate sorting
        