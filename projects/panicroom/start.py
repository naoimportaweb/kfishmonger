import sys, os, shutil, inspect, random, json;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.systemctl import Systemctl
from api.CONST import *;

def main():
    ctl = Systemctl( PANICROOM_SERVICE );
    ctl.start();
    if ctl.status():
        print("Está rodando os sistemas FAKE.");
    else:
        print("Os sistemas FAKE estão desligados.");

if __name__ == "__main__":
    main();
