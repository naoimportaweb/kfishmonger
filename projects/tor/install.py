import sys, os, shutil, inspect, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.systemctl import Systemctl;
from api.torrc import Torrc;


# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
apt = Apt()
apt.install("tor");

# =========== COPIA DE RESOURCES ==========================

# =========== INICIANDO SERVICOS E PROGRMAS ===============
ctl = Systemctl("tor.service");
ctl.reload();
ctl.stop();

# Tem que alterar o arquivo /etc/tor/torrc
torrc = Torrc();
torrc.runasdaemon();
torrc.tunnelport(9051);
torrc.save();

ctl.start();
ctl.enable();
time.sleep(2);
if ctl.status():
    print("Rodando");
else:
    print("Nao está rodando.");