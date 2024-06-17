import sys, os, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.systemctl import Systemctl;
from api.pip import Pip;
# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
pip = Pip();
pip.install("PySocks");
pip.install("requests");
# =========== COPIA DE RESOURCES ==========================

shutil.copy( CURRENTDIR + "/resources/json.service", "/etc/systemd/system/");

# =========== INICIANDO SERVICOS E PROGRMAS ===============
ctl = Systemctl("json.service");
ctl.reload();
ctl.start();
ctl.enable();
if ctl.status():
    print("Rodando");
else:
    print("Nao está rodando.");