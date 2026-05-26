import os, sys, uuid, requests, json, time;

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint, QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *

class PushStatusButton(QPushButton):
    def __init__(self, parent, str_icon_on, str_icon_off, default_status=False):
        super().__init__(parent);
        self.default_status = default_status;
        self.icon_on =  QIcon(); self.icon_on.addFile( str_icon_on,  QSize(), QIcon.Normal, QIcon.Off);
        self.icon_off = QIcon(); self.icon_off.addFile(str_icon_off, QSize(), QIcon.Normal, QIcon.Off);
        self.setMaximumWidth(30)
        if self.default_status:
            self.setIcon(self.icon_on);
        else:
            self.setIcon(self.icon_off);
    def setStatus(self, status):
        self.default_status = status;
        if self.default_status:
            self.setIcon(self.icon_on);
        else:
            self.setIcon(self.icon_off);
    def commut(self):
        self.setStatus( not self.default_status );
