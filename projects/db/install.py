import sys, os, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

#from api.apt import Apt;
from api.systemctl import Systemctl;
from api.log import Log;
from api.config_project import ConfigProject;
log = Log("db");
# =========== INSTALAÇÃO DE DEPENDENCIAS ==================

DIR_VAR = "/var/kfm";
if not os.path.exists(DIR_VAR):
    os.makedirs(DIR_VAR);
DIR_VAR = "/var/kfm/db";
if not os.path.exists(DIR_VAR):
    os.makedirs(DIR_VAR);

# =========== COPIA DE RESOURCES ==========================
config_project = ConfigProject("db", log=log);
config_project.copy();

shutil.copy( CURRENTDIR + "/resources/" + DB_SERVICE, "/etc/systemd/system/");

# =========== INICIANDO SERVICOS E PROGRMAS ===============
ctl = Systemctl( DB_SERVICE );
ctl.reload();
ctl.start();
ctl.enable();
if ctl.status():
    print("Rodando");
else:
    print("Nao está rodando.");