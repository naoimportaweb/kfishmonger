import sys, os, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.systemctl import Systemctl;
from api.resolv import Resolv;
from api.process import Process;

# =========== INICIANDO SERVICOS E PROGRMAS ===============
#ctl = Systemctl("kfm_dns.service");

r = Resolv();
r.clear();
r.add("nameserver 1.1.1.1");
r.save();


p = Process("pkill dnscrypt-proxy");
p.run();

#ctl.stop();





