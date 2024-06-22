import sys, os, shutil, inspect, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.systemctl import Systemctl;

# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
# Para o debian 11 e posterior: https://github.com/DNSCrypt/dnscrypt-proxy/wiki/Installation-on-Debian-and-Ubuntu#debian-testing-bullseye-debian-unstable-sid

# se existe vai direto
apt = Apt()
if not apt.instaled("dnscrypt-proxy"):
    if apt.exists("dnscrypt-proxy"):
        apt.addrepo("unstable"); # no Debian 12 foi colocado cono unstabe package
    apt.install("dnscrypt-proxy");

# =========== COPIA DE RESOURCES ==========================
shutil.copy( CURRENTDIR + "/resources/kfm_dns.service", "/etc/systemd/system/");

# =========== INICIANDO SERVICOS E PROGRMAS ===============
ctl = Systemctl("dnscrypt-proxy");
ctl.reload();
ctl.disable();

ctl = Systemctl("kfm_dns.service");
ctl.reload();
ctl.enable();
ctl.start();
if ctl.status():
    print("Está rodando o serviço DNS Crypt");
else:
    print("NÃO está rodando o serviço DNS Crypt");
