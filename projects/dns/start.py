import sys, os, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.process import Process;

# =========== INICIANDO SERVICOS E PROGRMAS ===============

p = Process("dnscrypt-proxy -config /etc/dnscrypt-proxy/dnscrypt-proxy.toml");
p.run();

