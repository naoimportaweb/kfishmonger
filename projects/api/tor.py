import os, sys;
import psutil

from process import Process;
from systemctl import Systemctl;
from CONST import *

class Tor(Systemctl):
    def __init__(self):
        super().__init__(TOR_SERVICE);