import sys, os, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.systemctl import Systemctl;

# =========== INICIANDO SERVICOS E PROGRMAS ===============
ctl = Systemctl("dnscrypt-proxy");
ctl.restart();

if ctl.status():
    print("Rodando DNS");
else:
    print("Nao está rodando.");
