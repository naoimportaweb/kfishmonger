import sys, os, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.systemctl import Systemctl;
from api.resolv import Resolv;
from api.process import Process;
from CONST import *;
# =========== INICIANDO SERVICOS E PROGRMAS ===============
#ctl = Systemctl("kfm_dns.service");

r = Resolv();
r.clear();
r.add("nameserver " + DNS_DEFAULT_RESOLVER);
r.save();

def main():
    ctl = Systemctl("kfm_dns.service");
    ctl.start();
    if ctl.status():
        print("Está rodando o serviço DNS Encrypt.");
    else:
        print("Sem DNS Encrypt.");

if __name__ == "__main__":
    main();

