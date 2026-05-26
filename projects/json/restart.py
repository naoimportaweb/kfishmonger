import sys, os, shutil, inspect, random, json;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.systemctl import Systemctl
from api.CONST import *;

def main():
    ctl = Systemctl( JSON_SERVICE );
    ctl.restart();
    if ctl.status():
        print("Está rodando o sistema JSON-CONKY.");
    else:
        print("O sistema JSON-CONKY está desligados.");

if __name__ == "__main__":
    main();



#import sys, os, shutil, inspect, random, json;
#CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
#ROOT = os.path.dirname(CURRENTDIR);
#sys.path.append(ROOT);
#from api.CONST import *;
#from api.systemctl import Systemctl
#def main():
#    ctl = Systemctl( VPN_SERVICE );
#    ctl.stop();
#    if ctl.status():
#        print("Está rodando a VPN.");
#    else:
#        print("A VPN está parada");
#    print("Reiniciando a VPN.");
#    ctl.start();
#    if ctl.status():
#        print("Está rodando a VPN.");
#    else:
#        print("A VPN está parada");
#if __name__ == "__main__":
#    main();
