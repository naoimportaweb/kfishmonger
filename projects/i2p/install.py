import sys, os, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.log import Log;
from api.CONST import *;
from api.distro import Distro;
from api.process import Process;

distro = Distro();
apt = Apt();
log = Log("i2p");
# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
apt.install("curl");
apt.install("lsb-release");
apt.install("apt-transport-https");
apt.install("software-properties-common");
with open("/etc/apt/sources.list.d/i2p.list", "w") as f:
    f.write("deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ "+ distro.release() +" main");
if not os.path.exists("/etc/apt/trusted.gpg.d/i2p-archive-keyring.gpg"):
    p = Process("curl -o /tmp/i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg");
    print(p.run());
    shutil.copy("/tmp/i2p-archive-keyring.gpg", "/usr/share/keyrings");
    os.symlink("/usr/share/keyrings/i2p-archive-keyring.gpg", "/etc/apt/trusted.gpg.d/i2p-archive-keyring.gpg")
apt.update();
apt.install("i2p");
if distro.name() == "debian":
    apt.install("i2p-keyring");

# =========== COPIA DE RESOURCES ==========================

# =========== INICIANDO SERVICOS E PROGRMAS ===============












#Instructions for Ubuntu and derivatives like Linux Mint & Trisquel
#sudo apt-get install software-properties-common
#sudo apt-add-repository ppa:i2p-maintainers/i2p
#sudo apt-get update
#sudo apt-get install i2p

#Instructions for Debian
#sudo apt-get install apt-transport-https lsb-release curl

#Check which version of Debian you are using on this page at the Debian wiki and verify with /etc/debian_version on your system. Then, for Debian Bullseye or newer distributions run the following command to create /etc/apt/sources.list.d/i2p.list.
#    # Use this command on Debian Bullseye or newer only.
#  echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" \
#  | sudo tee /etc/apt/sources.list.d/i2p.list
#If you're using a downstream variant of Debian like LMDE or Kali Linux, the following command fill find the correct version for your distribution:
#    # Use this command on Debian Downstreams like LMDE or ParrotOS only.
#  echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
#  | sudo tee /etc/apt/sources.list.d/i2p.list
#If you are using Debian Buster or older official Debian distributons, use the following command instead:
#    # Use this command on Debian Buster or older only.
#  echo "deb https://deb.i2p.net/ $(lsb_release -sc) main" \
#  | sudo tee /etc/apt/sources.list.d/i2p.list
#If you're using a downstream variant of Debian like LMDE or Kali Linux, the following command fill find the correct version for your distribution:
#    # Use this command on Debian Buster or older only.
#  echo "deb https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
#  | sudo tee /etc/apt/sources.list.d/i2p.list
    
#curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
#gpg --keyid-format long --import --import-options show-only --with-fingerprint i2p-archive-keyring.gpg
#sudo cp i2p-archive-keyring.gpg /usr/share/keyrings
#sudo ln -sf /usr/share/keyrings/i2p-archive-keyring.gpg /etc/apt/trusted.gpg.d/i2p-archive-keyring.gpg
#sudo apt-get update
#sudo apt-get install i2p i2p-keyring
