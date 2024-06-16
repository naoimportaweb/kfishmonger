import sys, os, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENTDIR)));
sys.path.append(ROOT);

from api.apt import Apt;
from api.systemctl import Systemctl;

# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
apt = Apt()
apt.install("conky");
apt.install("jp");

# =========== COPIA DE RESOURCES ==========================
directory_username_autostart = "/home/"+  os.getlogin()  +"/.config/autostart/";
if not os.path.exists( directory_username_autostart ):
	os.makedirs( directory_username_autostart );

shutil.copy( CURRENTDIR + "/resources/conky.desktop", directory_username_autostart);

# =========== INICIANDO SERVICOS E PROGRMAS ===============
#ctl = Systemctl("conky.service");
#ctl.reload();
#ctl.start();
#ctl.enable();
#if ctl.status():
#    print("Rodando");
#else:
#    print("Nao está rodando.");