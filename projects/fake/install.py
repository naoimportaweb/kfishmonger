import sys, os, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.systemctl import Systemctl;
from api.pip import Pip;
from api.log import Log;
from api.config_project import ConfigProject
from api.CONST import *;

log = Log("fake");
# =========== INSTALAÇÃO DE DEPENDENCIAS ==================

pip = Pip();
pip.install("paramiko");

# =========== COPIA DE RESOURCES ==========================
config_project = ConfigProject("fake", log=log);
config_project.copy();
config_project.execute = True;
config_project.save();

shutil.copy( CURRENTDIR + "/resources/" + FAKE_SERVICE, "/etc/systemd/system/");

# =========== INICIANDO SERVICOS E PROGRMAS ===============
ctl = Systemctl( FAKE_SERVICE , log=log);
ctl.reload();
ctl.start();
ctl.enable();
if ctl.status():
    print("Executando serviços FAKE");
else:
    print("NÃO está executando serviços FAKE");