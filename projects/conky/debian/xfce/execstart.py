import sys, os, shutil
import psutil, netifaces, json

sys.path.insert(0,"/opt/kfishmonger/projects/") 

print(sys.path);
from api.process import Process;
from api.config import Config;
from api.distro import Distro;

#p = Process("conky -d -c /opt/kfishmonger/projects/conky/debian/xfce/resources/conky.config");
#output = p.run();
#for linha in output:
#    print(linha);

shutil.copy( "/opt/kfishmonger/projects/conky/debian/xfce/resources/conky.config", "/tmp/conky.config");

#    ${goto 400}${voffset -360}${color3}${font pixelsize=18}VPN${font}${color0} ${downspeedgraph tun0}\
#    ${goto 400}${voffset 40  }${color3}${font pixelsize=18}ISP${font}${color0}   ${downspeedgraph enp0s3}\
texto = "";
dados_interfaces = psutil.net_io_counters(pernic=True)
interfaces = netifaces.interfaces();
for i in range(len( interfaces )):
    texto = texto + "\t${goto 400}${voffset 40}${color3}${font pixelsize=18}"+ interfaces[i] +"${font}${color0} ${downspeedgraph "+ interfaces[i] +"}\\\r\n";
    print(texto);
distro = Distro();
config = Config("/tmp/conky.config");
config.open();
config.replace("{INTERFACE}", distro.interfaces()[1]);
config.replace("{BARRA_INTERFACES}", texto);
config.save();

p = Process("conky -d -c /tmp/conky.config");
output = p.run();
for linha in output:
    print(linha);

