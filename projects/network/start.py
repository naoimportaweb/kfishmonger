import sys, os, shutil, inspect, random, json;

# Chamado no command line exemplo: sudo kfm -p dns -c start
#    ai esse script vem e atua no serviço, neste caso pedindo um start

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.systemctl import Systemctl
from api.CONST import *;

def main():
    ctl = Systemctl( NETWORK_SERVICE );
    ctl.start();
    if ctl.status():
        print("O serviço " + NETWORK_SERVICE + " está sendo executado.");
    else:
        print("O serviço " + NETWORK_SERVICE + " está PARADO.");

if __name__ == "__main__":
    main();
