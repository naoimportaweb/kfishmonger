
# temque DES-bloquear alteracao o /etc/resolv.conf
# tem que colocar nameservers 1.1.1.1 no /etc/resolv.conf
# temque bloquear alteracao o /etc/resolv.conf
# tem que eliminar as regras tun0

#sudo openvpn --config /home/ipv/conf/ipvanish-CA-Toronto-tor-a09.ovpn --auth-user-pass pass.txt
# pass.txt 'e um arquivo com usuario na primeira linha e senha na segunda linha'

import sys, os, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.process import Process;


directory_username = "/home/"+  os.environ["LOGNAME"]  +"/";
print("Path: ", directory_username);

path_password = directory_username +".vpn/pass.txt"
if os.path.exists(path_password):
    os.unlink( path_password );

with open(path_password, "w") as f:
    f.write( "VFFdx9Dj2J" + os.linesep );
    f.write( "zyswFpAMdp" + os.linesep );

if os.path.exists(directory_username +".vpn/openvpn.ovpn)":
    command = "/usr/sbin/openvpn --config "+ directory_username +".vpn/openvpn.ovpn --auth-user-pass " + path_password; 
    p = Process(command);
    print( p.run().read());

