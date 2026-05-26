import sys, os;

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint, QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *

sys.path.append(os.environ["ROOT"]);

from widget.page import Page;
from ui.tabwidget import TabWidget;
from ui.tablewidget import TableWidget;

class PageVpn(Page):
    def make(self):
        layout = QGridLayout()
        t = TabWidget(tabs=["Details", "Files .ovpn"]);
        layout.addWidget(t);

        js = [
            {"path" : "1"},{"path" : "2"}
        ];
        tl = TableWidget();
        tl.addHead("path", "Path", resize=True);
        tl.setData(js);
        t.addTabWidget( 1, tl );
        self.setLayout(layout)
        return None;