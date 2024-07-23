import sys, os, shutil, inspect, getpass;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR));
sys.path.append(ROOT);

from api.apt import Apt;
from api.pip import Pip;
from api.systemctl import Systemctl;
from api.distro import Distro;
from api.config import Config;

distro = Distro();

# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
apt = Apt();
pip = Pip();
pip.install("psutil");
pip.install("netifaces");

# =========== COPIA DE RESOURCES ==========================
directory_username_autostart = "/home/"+  distro.user()  +"/.config/autostart/";

if not os.path.exists( directory_username_autostart ):
    os.makedirs( directory_username_autostart );

shutil.copy( CURRENTDIR + "/" + distro.graphical() + "/resources/conky.desktop", directory_username_autostart);

