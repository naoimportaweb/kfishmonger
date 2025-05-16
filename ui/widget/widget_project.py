import os, sys, uuid;

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint, QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *

class ProjectWidget(QWidget):
    def make(self):
        self.hlayout = QHBoxLayout(self)
        self.btn_start_stop = QPushButton(self)
        self.btn_start_stop.setObjectName(u"btn_start_stop")
        icon2 = QIcon()
        icon2.addFile(u":/16x16/icons/16x16/cil-x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_start_stop.setIcon(icon2)
        self.hlayout.addWidget(self.btn_start_stop)
        return None;
