import sys, os, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.systemctl import Systemctl;
from api.log import Log;
from api.config_project import ConfigProject
from api.CONST import *;

log = Log("network");
# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
apt = Apt(log=log);
apt.install("net-tools");

# =========== COPIA DE RESOURCES ==========================
config_project = ConfigProject("network", log=log);
config_project.copy();

shutil.copy( CURRENTDIR + "/resources/" + NETWORK_SERVICE, "/etc/systemd/system/");

# =========== INICIANDO SERVICOS E PROGRMAS ===============
ctl = Systemctl( NETWORK_SERVICE );
ctl.reload();
ctl.start();
ctl.enable();
if ctl.status():
    print("Rodando Network");
else:
    print("Nao está rodando.");