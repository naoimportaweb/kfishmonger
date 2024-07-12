import sys, os, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.systemctl import Systemctl;
from api.pip import Pip;
from api.log import Log;
from api.config_project import ConfigProject

log = Log("json");
# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
pip = Pip();
pip.install("PySocks");
pip.install("requests");
# =========== COPIA DE RESOURCES ==========================
config_project = ConfigProject("json", log=log);
config_project.copy();

shutil.copy( CURRENTDIR + "/resources/json.service", "/etc/systemd/system/");

# =========== INICIANDO SERVICOS E PROGRMAS ===============
ctl = Systemctl("json.service", log=log);
ctl.reload();
ctl.start();
ctl.enable();
if ctl.status():
    print("Rodando");
else:
    print("Nao está rodando.");