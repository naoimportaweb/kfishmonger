import sys, os, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.process import Process;
from api.resolv import Resolv
# =========== INICIANDO SERVICOS E PROGRMAS ===============


def callbakc_retorno(process, ret):
    print(ret);
p = Process("python3 " + CURRENTDIR + "/sub/monitor.py");
p.asThread(callbakc_retorno);

process = Process("/etc/dnscrypt-proxy/linux-x86_64/dnscrypt-proxy -config /etc/dnscrypt-proxy/linux-x86_64/dnscrypt-proxy.toml");
process.run();
