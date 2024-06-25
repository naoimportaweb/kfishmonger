import sys, os, shutil, inspect, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.systemctl import Systemctl;
from api.distro import Distro;
from api.process import Process;
# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
# Para o debian 11 e posterior: https://github.com/DNSCrypt/dnscrypt-proxy/wiki/Installation-on-Debian-and-Ubuntu#debian-testing-bullseye-debian-unstable-sid

if os.path.exists("/etc/dnscrypt-proxy/linux-x86_64/dnscrypt-proxy"):
    print("Já está instalado.");
    #sys.exit(0);

# se existe vai direto
apt = Apt()
distro = Distro();

remover = ["/tmp/linux-x86_64", "/tmp/dnscrypt-proxy-linux_x86_64-2.0.45.tar.gz" ];
for arquivo in remover:
    if os.path.exists(arquivo):
        if os.path.isdir(arquivo):
            shutil.rmtree(arquivo, ignore_errors=True)
        else:
            os.unlink(arquivo);
#if apt.instaled( "dnscrypt-proxy" ):
#    apt.purge( "dnscrypt-proxy" );

process = Process("wget https://github.com/DNSCrypt/dnscrypt-proxy/releases/download/2.0.45/dnscrypt-proxy-linux_x86_64-2.0.45.tar.gz -O /tmp/dnscrypt-proxy-linux_x86_64-2.0.45.tar.gz");
process.run();
process = Process("mkdir /tmp/linux-x86_64");
process.run();
process = Process("tar --strip-components 1 -C /tmp/linux-x86_64/ -xzf /tmp/dnscrypt-proxy-linux_x86_64-2.0.45.tar.gz");
process.run();
process = Process("mkdir /etc/dnscrypt-proxy");
process.run();
process = Process("cp -r /tmp/linux-x86_64/ /etc/dnscrypt-proxy/");
process.run();
process = Process("cp /etc/dnscrypt-proxy/linux-x86_64/example-dnscrypt-proxy.toml /etc/dnscrypt-proxy/linux-x86_64/dnscrypt-proxy.toml");
process.run();

shutil.copy( CURRENTDIR + "/resources/kfm_dns.service", "/etc/systemd/system/");
shutil.copy( CURRENTDIR + "/resources/dnscrypt-proxy.toml", "/etc/dnscrypt-proxy/linux-x86_64/");

ctl = Systemctl("kfm_dns.service");
ctl.reload();
ctl.enable();
ctl.start();
if ctl.status():
    print("Está rodando o serviço DNS Crypt");
else:
    print("NÃO está rodando o serviço DNS Crypt");

ctl = Systemctl("dnscrypt-proxy");
if ctl.exists():
    ctl.disable();
    ctl.stop();