
# temque DES-bloquear alteracao o /etc/resolv.conf
# tem que colocar nameservers 1.1.1.1 no /etc/resolv.conf
# temque bloquear alteracao o /etc/resolv.conf
# tem que eliminar as regras tun0

#sudo openvpn --config /home/ipv/conf/ipvanish-CA-Toronto-tor-a09.ovpn --auth-user-pass pass.txt
# pass.txt 'e um arquivo com usuario na primeira linha e senha na segunda linha'

import sys, os, shutil, inspect, random, json;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.process import Process;
from api.distro import Distro;
from vpn.api.openvpn import Openvpn;
from api.log import Log;

distro = Distro();
log = Log("vpn");

def setmac(interface):
    p = Process("sudo ip link set "+ interface +" down"); p.run();
    novo_mac_address = "%02x:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) );
    log.info("Novo mac address " + novo_mac_address + " para interface " + interface);
    p = Process("sudo ip link set "+ interface +" address " + novo_mac_address); p.run();
    p = Process("sudo ip link set "+ interface +" up"); p.run();

def main():
    directory_username = "/var/kfm/vpn";
    ovpn = Openvpn();
    ovpn.loadrandom();
    ovpn.save();
    log.info("Será usada a VPN: "+  ovpn.eleito);

    path_configuracao = directory_username +"/config.json";
    json_config = {};

    if os.path.exists(path_configuracao):
        json_config = json.loads( open(path_configuracao).read() );

    path_password = directory_username +"/pass.txt"

    if os.path.exists(directory_username +"/openvpn.ovpn"):
        # set mackaddress
        if json_config.get("mac") != None:
            for interface in json_config["mac"]:
                setmac( interface );
        log.info("VPN será inicializada.");
        command = "/usr/sbin/openvpn --config "+ directory_username +"/openvpn.ovpn --auth-user-pass " + path_password; 
        p = Process(command, wait=False);
        print( p.run() );

if __name__ == "__main__":
    main();