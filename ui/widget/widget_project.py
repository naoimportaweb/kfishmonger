import os, sys, uuid, requests, json, time;

import threading

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint, QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *

sys.path.append(os.environ["ROOT"]);
sys.path.append( os.path.dirname(os.environ["ROOT"]) + "/projects/api/" );

from vpn import Vpn;

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


class ProjectWidget(QWidget):
    def make(self):
        layout = QGridLayout()
        self.btn_start_stop = PushStatusButton(self, u":/16x16/icons/16x16/cil-check.png", u":/16x16/icons/16x16/cil-power-standby.png");
        BUTTON_SIZE = QSize(30, 100);
        self.btn_start_stop.setMaximumSize(BUTTON_SIZE);
        layout.addWidget(self.btn_start_stop, 0, 0, 2, 1);

        label_service = QLabel(self)
        label_service.setObjectName(u"label_service")
        label_service.setText("VPN");
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(20)
        font1.setBold(True)
        label_service.setFont(font1)
        label_service.setStyleSheet(u"background: transparent;")
        layout.addWidget(label_service, 0, 1)

        self.label_country = QLabel(self)
        self.label_country.setObjectName(u"label_country")
        self.label_country.setText("-");
        layout.addWidget(self.label_country, 1, 1)

        self.setMaximumHeight(100)
        self.setLayout(layout)
        threading.Thread(target=self.montitor, args=()).start();
        return None;
    
    def montitor(self):
        while True:
            r = requests.get("https://wtfismyip.com/json");
            js_myip = json.loads(r.text);
            service = Vpn();
            self.btn_start_stop.setStatus(service.tunnel())
            self.label_country.setText(js_myip["YourFuckingIPAddress"] + " ("+ js_myip["YourFuckingCountry"] +")"  );
            time.sleep(60);
