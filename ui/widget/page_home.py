import sys, os;

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint, QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *

sys.path.append(os.environ["ROOT"]);

from widget.page import Page;
from widget.widget_vpn import ProjectVpn;
from widget.widget_tor import ProjectTor;
from widget.widget_dns import ProjectDns;

class PageHome(Page):
    def make(self):
        self.setObjectName(u"page_home")
        self.verticalLayout_10 = QVBoxLayout(self)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        frame_layouts = QFrame();
        buffer1 = ProjectVpn();
        buffer1.make();
        buffer2 = ProjectTor();
        buffer2.make();
        buffer3 = ProjectDns();
        buffer3.make();
        project_layouts = QVBoxLayout(frame_layouts);
        project_layouts.addWidget( buffer1 );
        project_layouts.addWidget( buffer2 );
        project_layouts.addWidget( buffer3 );
        frame_layouts.setLayout( project_layouts );
        self.verticalLayout_10.addWidget( frame_layouts );
        self.verticalLayout_10.addStretch();
        self.setLayout(self.verticalLayout_10);
        return self;

