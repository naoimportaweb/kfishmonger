import sys
from PySide6.QtWidgets import QWidget, QTabWidget, QFormLayout, QVBoxLayout, QLineEdit, QHBoxLayout, QRadioButton, QLabel, QCheckBox

class TabWidget(QTabWidget):
    def __init__(self, parent=None, tabs=None):
        super().__init__(parent)
        self.tabpages = [];
        if tabs != None:
            for tab in tabs:
                self.tabpages.append( self.add(tab) );
    
    def addTabWidget(self, tab, element):
        self.tabpages[tab].layout().addWidget( element );

    def add(self, title):
        tab = QWidget();
        tab.setLayout( QVBoxLayout() );
        self.addTab(tab, title);
        return tab;
