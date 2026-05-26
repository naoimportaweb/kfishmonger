import os, sys

from PySide6.QtWidgets import QWidget, QTableWidget,QTableWidgetItem, QHeaderView, QAbstractItemView

 
class TableWidget(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.data = [];
        self.headers = [];
        self.keys = [];
        self.setSelectionBehavior(QAbstractItemView.SelectRows); 
        self.setColumnCount(0);
        self.setEditTriggers(QAbstractItemView.NoEditTriggers);
        self.setHorizontalHeaderLabels(self.headers);
    
    def addHead(self, key, title, resize=False):
        self.headers.append( title );
        self.keys.append(    key );
        self.setColumnCount(len(self.headers));
        self.setHorizontalHeaderLabels(self.headers);
        if resize:
            self.horizontalHeader().setSectionResizeMode( len(self.headers) -1 , QHeaderView.ResizeToContents);
        else:
            self.horizontalHeader().setSectionResizeMode( len(self.headers) -1 , QHeaderView.Stretch);

    def setData(self, data): 
        self.data = data;
        self.setRowCount( len( self.data ) );
        for i in range(len(self.data)):
            keys = self.data[i].keys();
            for key in keys:
                index_j = self.keys.index( key );
                if index_j >= 0:
                    self.setItem( i , index_j, QTableWidgetItem( self.data[i][key] ) );
