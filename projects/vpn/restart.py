import sys, os, shutil, inspect, random, json;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.systemctl import Systemctl
from CONST import *;

def main():
    ctl = Systemctl( VPN_SERVICE );
    ctl.restart();
    if ctl.status():
        print("Está rodando a VPN.");
    else:
        print("A VPN está parada");

if __name__ == "__main__":
    main();
