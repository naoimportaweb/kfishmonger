import sys, os, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

#from api.apt import Apt;
from api.systemctl import Systemctl;
#from api.pip import Pip;
# =========== INSTALAÇÃO DE DEPENDENCIAS ==================

DIR_VAR = "/var/kfm";
if not os.path.exists(DIR_VAR):
    os.makedirs(DIR_VAR);
DIR_VAR = "/var/kfm/db";
if not os.path.exists(DIR_VAR):
    os.makedirs(DIR_VAR);

# =========== COPIA DE RESOURCES ==========================

shutil.copy( CURRENTDIR + "/resources/kfm_db.service", "/etc/systemd/system/");

# =========== INICIANDO SERVICOS E PROGRMAS ===============
ctl = Systemctl("kfm_db.service");
ctl.reload();
ctl.start();
ctl.enable();
if ctl.status():
    print("Rodando");
else:
    print("Nao está rodando.");