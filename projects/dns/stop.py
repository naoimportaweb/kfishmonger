import sys, os, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.systemctl import Systemctl;
from api.resolv import Resolv;
from api.distro import Distro;
from api.process import Process;
from api.CONST import *

# =========== INICIANDO SERVICOS E PROGRMAS ===============

# Em Qubes nao tocamos no resolv.conf (gerenciado pela NetVM); ver start.py.
if Distro().is_qubes():
    print("Qubes detectado: preservando o /etc/resolv.conf da NetVM.");
else:
    r = Resolv();
    r.clear();
    r.add("nameserver " + DNS_DEFAULT_RESOLVER);
    r.save();


p = Process("pkill dnscrypt-proxy");
p.run();

#ctl.stop();





