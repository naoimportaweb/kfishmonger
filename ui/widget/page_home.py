import sys, os;

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint, QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *

sys.path.append(os.environ["ROOT"]);

from widget.page import Page;

class PageHome(Page):
    def make(self):
        self.setObjectName(u"page_home")
        self.verticalLayout_10 = QVBoxLayout(self)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_6 = QLabel(self)
        self.label_6.setObjectName(u"label_6")
        font5 = QFont()
        font5.setFamily(u"Segoe UI")
        font5.setPointSize(40)
        self.label_6.setFont(font5)
        self.label_6.setStyleSheet(u"")
        self.label_6.setAlignment(Qt.AlignCenter)
        self.verticalLayout_10.addWidget(self.label_6)
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        font6 = QFont();
        font6.setFamily(u"Segoe UI");
        font6.setPointSize(14);
        self.label.setFont(font6);
        self.label.setAlignment(Qt.AlignCenter);
        self.verticalLayout_10.addWidget(self.label);
        self.label_7 = QLabel(self);
        self.label_7.setObjectName(u"label_7");
        font7 = QFont();
        font7.setFamily(u"Segoe UI");
        font7.setPointSize(15);
        self.label_7.setFont(font7);
        self.label_7.setAlignment(Qt.AlignCenter);
        self.verticalLayout_10.addWidget(self.label_7);
        # https://pt.stackoverflow.com/questions/85/como-utilizar-tradu%C3%A7%C3%B5es-em-qt-diretamente-com-qapplicationtr
        self.label_6.setText("Home");
        self.label.setText("Empyt Page");
        self.label_7.setText("Page Index 1");
        self.setLayout(self.verticalLayout_10);
        return self;

