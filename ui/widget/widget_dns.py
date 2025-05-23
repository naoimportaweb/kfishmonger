import os, sys, uuid, requests, json, time, socks, threading, socket;

from urllib3 import PoolManager
from urllib3.contrib.socks import SOCKSProxyManager

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint, QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *

sys.path.append(os.environ["ROOT"]);
sys.path.append( os.path.dirname(os.environ["ROOT"]) + "/projects/api/" );

from widget.push_status_button import PushStatusButton;

class ProjectDns(QWidget):
    def make(self):
        layout = QGridLayout()
        self.btn_start_stop = PushStatusButton(self, u":/16x16/icons/16x16/cil-check.png", u":/16x16/icons/16x16/cil-power-standby.png");
        BUTTON_SIZE = QSize(30, 100);
        self.btn_start_stop.setMaximumSize(BUTTON_SIZE);
        self.btn_start_stop.clicked.connect(self.btn_start_stop_clicked)
        layout.addWidget(self.btn_start_stop, 0, 0, 2, 1);

        label_service = QLabel(self)
        label_service.setObjectName(u"label_service")
        label_service.setText("DNS");
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(20)
        font1.setBold(True)
        label_service.setFont(font1)
        label_service.setStyleSheet(u"background: transparent;")
        layout.addWidget(label_service, 0, 1)

        self.setMaximumHeight(100)
        self.setLayout(layout)
        threading.Thread(target=self.montitor, args=()).start();
        return None;
    
    def btn_start_stop_clicked(self):
        service = Tor();
        if self.btn_start_stop.default_status:
            service.stop();
        else:
            service.start();
        #self.label_country.setText("WAITING...");

    def montitor(self):
        while True:
            time.sleep(30);
