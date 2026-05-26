import sys, os, shutil, inspect, random, json, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);
sys.path.append("/opt/kfishmonger/projects/vpn/");

from api.process import Process;
from api.distro import Distro;
from api.openvpn import Openvpn;
from api.log import Log;
from api.config_project import ConfigProject;
from api.resolv import Resolv;
from api.CONST import *

distro = Distro();
log = Log("vpn");
config = ConfigProject("vpn", log=log);
config.load();

def random_bytes(num=6):
    return [random.randrange(256) for _ in range(num)]

def generate_mac(uaa=False, multicast=False, oui=None, separator=':', byte_fmt='%02x'):
    if oui != None:
        return  oui + ":%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) );
    else:
        return "%02x:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) );

# LISTA DE POSSÍVEIS MAC: https://gist.github.com/NullArray/0380871a42b608830357f998df735e71
def setmac(interface, oui_default="08:00:27"):
    p = Process("sudo ip link set "+ interface +" down"); p.run();
    novo_mac_address = generate_mac(oui=oui_default);
    log.info("Novo mac address " + novo_mac_address + " para interface " + interface);
    p = Process("sudo ip link set "+ interface +" address " + novo_mac_address); p.run();
    p = Process("sudo ip link set "+ interface +" up"); p.run();

def main():
    directory_username = "/var/kfm/vpn";
    ovpn = Openvpn();
    if not ovpn.loadrandom():
        log.error("Não foi possível encontrar uma configuração válida para VPN.");
        return;
    ovpn.save();
    log.info("Será usada a VPN: "+  ovpn.eleito);

    if os.path.exists(directory_username +"/openvpn.ovpn"):
        path_password = directory_username +"/pass.txt";
        if len(config.mac) > 0:
            for interface in config.mac:
                oui = None;
                if len(config.oui) > 0:
                    oui = config.oui[ random.randint(0, len(config.oui) - 1 ) ];
                else:
                    oui = "08:00:27";
                setmac( interface, oui_default=oui );
                time.sleep(1);
        log.info("VPN será inicializada em poucos segundos.");
        r = Resolv();
        r.add("nameserver " + DNS_DEFAULT_RESOLVER);
        r.save();
        r.block();
        command = "/usr/sbin/openvpn --config "+ directory_username +"/openvpn.ovpn --auth-user-pass " + path_password; 
        p = Process(command, wait=False);
        print( p.run() );

if __name__ == "__main__":
    main();

# temque DES-bloquear alteracao o /etc/resolv.conf
# tem que colocar nameservers 1.1.1.1 no /etc/resolv.conf
# temque bloquear alteracao o /etc/resolv.conf
# tem que eliminar as regras tun0

#sudo openvpn --config /home/ipv/conf/ipvanish-CA-Toronto-tor-a09.ovpn --auth-user-pass pass.txt
# pass.txt 'e um arquivo com usuario na primeira linha e senha na segunda linha'