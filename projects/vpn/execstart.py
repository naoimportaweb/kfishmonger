import sys, os, shutil, inspect, random, json, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.process import Process;
from api.distro import Distro;
from vpn.api.openvpn import Openvpn;
from api.log import Log;
from api.config_project import ConfigProject;

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
    #mac = random_bytes()
    #if oui:
    #    if type(oui) == str:
    #        oui = [int(chunk) for chunk in oui.split(separator)]
    #    mac = oui + random_bytes(num=6-len(oui))
    #else:
    #    if multicast:
    #        mac[0] |= 1 # set bit 0
    #    else:
    #        mac[0] &= ~1 # clear bit 0
    #    if uaa:
    #        mac[0] &= ~(1 << 1) # clear bit 1
    #    else:
    #        mac[0] |= 1 << 1 # set bit 1
    #return separator.join(byte_fmt % b for b in mac)

# LISTA DE POSSÍVEIS MAC: https://gist.github.com/NullArray/0380871a42b608830357f998df735e71
def setmac(interface, oui_default="08:00:27"):
    p = Process("sudo ip link set "+ interface +" down"); p.run();
    novo_mac_address = generate_mac(oui=oui_default);
    log.info("Novo mac address " + novo_mac_address + " para interface " + interface);
    p = Process("sudo ip link set "+ interface +" address " + novo_mac_address); p.run();
    p = Process("sudo ip link set "+ interface +" up"); p.run();

def main():
    if config.execute == False:
        log.info("A VPN está desabilitada no arquivo /var/kfm/vpn/config.json.");
        return;
    directory_username = "/var/kfm/vpn";
    ovpn = Openvpn();
    if not ovpn.loadrandom():
        log.error("Não foi possível encontrar uma configuração válida para VPN.");
        return;
    ovpn.save();
    log.info("Será usada a VPN: "+  ovpn.eleito);

    #path_configuracao = directory_username +"/config.json";
    #json_config = {};

    #if os.path.exists(path_configuracao):
    #    log.info("Existe um arquivo de configuração extra para a VPN.");
    #    json_config = json.loads( open(path_configuracao).read() );
    #else:
    #    log.info("NÃO Existe um arquivo de configuração extra para a VPN.");

    
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