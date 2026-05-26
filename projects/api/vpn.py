import os, sys;
import psutil

from process import Process;
from systemctl import Systemctl;
from CONST import *

class Vpn(Systemctl):
    def __init__(self):
        super().__init__(VPN_SERVICE);
        self.dir_config = "/var/kfm/vpn/";
        self.configs = [];
    
    def tunnel(self):
        addrs = psutil.net_if_addrs()
        for interface_name in addrs:
            if interface_name[:3] == "tun":
                return True;
        return False;

    def configs(self):
        files = os.listdir( self.dir_config );
        for file in files:
            path_buffer = os.path.join( self.dir_config, file ) ;
            if os.path.isdir( path_buffer ) and self.text( path_buffer ):
            	self.configs.append( path_buffer );
        return self.configs;
        
    def test(self, dir_path):
        path_ovpn = os.path.join( dir_path, "openvpn.ovpn" );
        path_pass = os.path.join( dir_path, "pass.txt" );
        return os.path.exists(path_ovpn) and os.path.exists(path_pass);
