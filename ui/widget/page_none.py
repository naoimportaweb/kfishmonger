import os, sys, uuid, requests, json, time;

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint, QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *

sys.path.append(os.environ["ROOT"]);
sys.path.append( os.path.dirname(os.environ["ROOT"]) + "/projects/api/" );

class PageNone(QWidget):
    def make(self):
        layout = QGridLayout()
        self.setLayout(layout)
        
    