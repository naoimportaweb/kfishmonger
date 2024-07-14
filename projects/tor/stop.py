import sys, os, shutil, inspect, random, json;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.systemctl import Systemctl
from CONST import *;

def main():
    ctl = Systemctl( TOR_SERVICE );
    ctl.stop();
    if ctl.status():
        print("O TOR está sendo executado.");
    else:
        print("O TOR está PARADO");

if __name__ == "__main__":
    main();