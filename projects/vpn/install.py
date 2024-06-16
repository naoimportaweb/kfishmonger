import sys, os, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.systemctl import Systemctl;
from api.config import Config;

directory_username = "/home/"+  os.getlogin()  +"/";

# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
apt = Apt()
apt.install("openvpn");

# =========== COPIA DE RESOURCES ==========================
shutil.copy( CURRENTDIR + "/resources/vpn.service", "/etc/systemd/system/");
if not os.path.exists( directory_username + "/.vpn" ):
    os.makedirs(directory_username + "/.vpn");

config = Config(directory_username + "/.vpn/user.txt");
if not config.findattribute("user"):
    config.addattribute("user");
    config.save();
if not config.findattribute("password"):
    config.addattribute("password");
    config.save();


# =========== SERVICE ==========================
ctl = Systemctl("vpn.service");
ctl.reload();
ctl.start();
ctl.enable();
if ctl.status():
    print("Rodando");
else:
    print("Nao está rodando.");