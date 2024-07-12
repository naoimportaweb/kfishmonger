import sys, os, shutil, time, hashlib, netifaces, json, traceback

sys.path.insert(0,"/opt/kfishmonger/projects/");

from api.process import Process;
from api.systemctl import Systemctl

from api.log import Log;
log = Log("anonsurf");

s = Systemctl("vpn.service");
if s.running():
    p = Process("anonsurf", wait=False);
    log.info("Iniciando Anonsurf");
    print( p.run() );
else:
    log.info("O script Anonsurf não pode ser executado pois a VPN está ligada.");

