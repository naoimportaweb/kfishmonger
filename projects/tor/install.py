import sys, os, shutil, inspect, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.systemctl import Systemctl;
from api.torrc import Torrc;
from api.config_project import ConfigProject
from api.log import Log;

# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
log = Log("vpn");
apt = Apt(log=log)
apt.install("tor");

# =========== COPIA DE RESOURCES ==========================

# =========== ARQUIVO DE CONFIGURAÇAO DO SERVIÇO ==========================

config_project = ConfigProject("tor", log=log);
config_project.copy();

# =========== INICIANDO SERVICOS E PROGRMAS ===============
ctl = Systemctl("tor.service");
ctl.reload();
ctl.stop();

# Tem que alterar o arquivo /etc/tor/torrc
torrc = Torrc();
torrc.runasdaemon();
torrc.tunnelport(9051);
torrc.exclude14eyes();
torrc.virtualnetwork();
torrc.trasnport();
torrc.hostsonresolve();
torrc.socksport();
torrc.dnsport();
torrc.save();

ctl.start();
ctl.enable();
time.sleep(2);
if ctl.status():
    print("Rodando");
else:
    print("Nao está rodando.");



