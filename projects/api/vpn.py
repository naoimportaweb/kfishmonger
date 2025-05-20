import os, sys;
import psutil


from process import Process;
from systemctl import Systemctl;
from CONST import *

class Vpn(Systemctl):
	def __init__(self):
		super().__init__(VPN_SERVICE);
	def tunnel(self):
		addrs = psutil.net_if_addrs()
		for interface_name in addrs:
			if interface_name[:3] == "tun":
				return True;
		return False;