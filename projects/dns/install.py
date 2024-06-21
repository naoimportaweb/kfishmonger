import sys, os, shutil, inspect, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.systemctl import Systemctl;

# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
apt = Apt()
apt.install("dnscrypt-proxy");

# =========== COPIA DE RESOURCES ==========================



# =========== INICIANDO SERVICOS E PROGRMAS ===============
ctl = Systemctl("dnscrypt-proxy");
ctl.reload();
ctl.enable();
ctl.start();

if ctl.status():
    print("Rodando");
else:
    print("Nao está rodando.");
