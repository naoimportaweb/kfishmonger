import sys, os, shutil, inspect, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.systemctl import Systemctl;
from api.distro import Distro;

# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
# Para o debian 11 e posterior: https://github.com/DNSCrypt/dnscrypt-proxy/wiki/Installation-on-Debian-and-Ubuntu#debian-testing-bullseye-debian-unstable-sid

# se existe vai direto
apt = Apt()
distro = Distro();

process = Process("wget https://github.com/DNSCrypt/dnscrypt-proxy/releases/download/2.0.45/dnscrypt-proxy-linux_x86_64-2.0.45.tar.gz -O /tmp/dnscrypt-proxy-linux_x86_64-2.0.45.tar.gz");
process.run();

process = Process("tar -C /tmp/ -xzf /tmp/dnscrypt-proxy-linux_x86_64-2.0.45.tar.gz");
process.run();

process = Process("mkdir /etc/dnscrypt-proxy");
process.run();

process = Process("cp -r /tmp/linux-x86_64/* /etc/dnscrypt-proxy/");
process.run();

process = Process("cp /etc/dnscrypt-proxy/example-dnscrypt-proxy.toml /etc/dnscrypt-proxy/dnscrypt-proxy.toml");
process.run();

shutil.copy( CURRENTDIR + "/resources/kfm_dns.service", "/etc/systemd/system/");

ctl = Systemctl("kfm_dns.service");
ctl.reload();
ctl.enable();
ctl.start();
if ctl.status():
    print("Está rodando o serviço DNS Crypt");
else:
    print("NÃO está rodando o serviço DNS Crypt");

#if not apt.instaled("dnscrypt-proxy"):
#    if distro.name() == "debian":
#        apt.addrepo("unstable");
#    apt.install("dnscrypt-proxy");
#if apt.instaled("dnscrypt-proxy"):
#    # =========== COPIA DE RESOURCES ==========================
#    shutil.copy( CURRENTDIR + "/resources/kfm_dns.service", "/etc/systemd/system/");
#
#    # =========== INICIANDO SERVICOS E PROGRMAS ===============
#    ctl = Systemctl("dnscrypt-proxy");
#    ctl.reload();
#    ctl.disable();
#
#    ctl = Systemctl("kfm_dns.service");
#    ctl.reload();
#    ctl.enable();
#    ctl.start();
#    if ctl.status():
#        print("Está rodando o serviço DNS Crypt");
#    else:
#        print("NÃO está rodando o serviço DNS Crypt");
#else:
#    print("Não fo i possível instalar o dnscrypt");
