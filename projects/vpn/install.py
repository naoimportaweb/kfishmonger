import sys, os, shutil, inspect, getpass;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.systemctl import Systemctl;
from api.config import Config;
from api.process import Process;
from api.distro import Distro;
from api.log import Log;
from api.config_project import ConfigProject
from api.CONST import *;

distro = Distro();
log = Log("vpn");
apt = Apt(log=log)

directory_username = "/home/"+  distro.user()  +"/";

# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
apt.install("openvpn");

# =========== COPIA DE RESOURCES ==========================
shutil.copy( CURRENTDIR + "/resources/vpn.service", "/etc/systemd/system/");

config = Config("/etc/systemd/system/vpn.service");
config.open();
config.replace("{LOGNAME}", distro.user() );
config.save();

# =========== CRIANDO DIRETORIOS ==========================
if not os.path.exists("/var/kfm/vpn"):
    os.makedirs("/var/kfm/vpn");
    log.info("Criando o diretório /var/kfm/vpn");

# =========== ARQUIVO DE CONFIGURAÇAO DO SERVIÇO ==========================

config_project = ConfigProject("vpn", log=log);
config_project.copy();

# =========== IMPORTANDO VERSÃO ANTIGA DA VPN ==========================
if os.path.exists( directory_username + "/.vpn" ):
    files = os.listdir(directory_username + "/.vpn/");
    for item in files:
        shutil.copy( directory_username + "/.vpn/" + item, "/var/kfm/vpn/" )
        os.unlink(directory_username + "/.vpn/" + item);
    shutil.rmtree(directory_username + "/.vpn", ignore_errors=False);

# =========== DESABILITAR O IPV6 PARA NÃO EXPOR =================

config = Config("/etc/sysctl.conf");
config.open();
config.addattribute("net.ipv6.conf.all.disable_ipv6",       value= "1");
config.addattribute("net.ipv6.conf.default.disable_ipv6",   value= "1");
config.addattribute("net.ipv6.conf.lo.disable_ipv6",        value= "1");
config.save();

# =========== SERVICE ==========================
ctl = Systemctl( VPN_SERVICE );
ctl.reload();
ctl.start();
ctl.enable();
if ctl.status():
    print("Rodando");
    log.info("VPN está sendo executado normalmente.");
else:
    print("Nao está rodando.");
    log.error("Não foi possível rodar a VPN.");