import sys, os, shutil, time
import netifaces, json

sys.path.insert(0,"/opt/kfishmonger/projects/") 

from api.process import Process;
from api.config import Config;
from api.distro import Distro;

# uma pausa de 30 segundos para carregar vpn e tor.
time.sleep(30);

shutil.copy( "/opt/kfishmonger/projects/conky/resources/conky.config", "/tmp/conky.config");

texto = "";
#dados_interfaces = psutil.net_io_counters(pernic=True)
interfaces = netifaces.interfaces();
maior_tamanho_carateres = 0;
for i in range(len( interfaces )):
    if maior_tamanho_carateres < len(interfaces[i]):
        maior_tamanho_carateres  = len(interfaces[i]);
for i in range(len( interfaces )):
    texto = texto + "\t${goto 400}${voffset 30}${color3}${font pixelsize=18}"+ interfaces[i].ljust(maior_tamanho_carateres) +"${font}${color0} ${downspeedgraph "+ interfaces[i] +"}\\\r\n";

distro = Distro();
config = Config("/tmp/conky.config");
config.open();
config.replace("{INTERFACE}", distro.interfaces()[1]);
config.replace("{BARRA_INTERFACES}", texto);
config.save();

p = Process("conky -d -c /tmp/conky.config");
output = p.run();
#for linha in output:
#    print(linha);

