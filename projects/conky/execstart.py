import sys, os, shutil, time
import netifaces, json, traceback

sys.path.insert(0,"/opt/kfishmonger/projects/") 

from threading import Thread
from api.process import Process;
from api.config import Config;
from api.distro import Distro;

def documento():
    while True:
        try:
            shutil.copy( "/opt/kfishmonger/projects/conky/resources/conky.config", "/tmp/conky.buffer.config");
            p = Process("chmod 666 /tmp/conky.config");
            p.run();

            texto = "";
            interfaces = netifaces.interfaces();
            maior_tamanho_carateres = 0;
            for i in range(len( interfaces )):
                if maior_tamanho_carateres < len(interfaces[i]):
                    maior_tamanho_carateres  = len(interfaces[i]);
            for i in range(len( interfaces )):
                texto = texto + "\t${goto 400}${voffset 30}${color3}${font pixelsize=18}"+ interfaces[i].ljust(maior_tamanho_carateres) +"${font}${color0} ${downspeedgraph "+ interfaces[i] +"}\\\r\n";

            distro = Distro();
            config = Config("/tmp/conky.buffer.config");
            config.open();
            config.replace("{INTERFACE}", distro.interfaces()[1]);
            config.replace("{BARRA_INTERFACES}", texto);
            if not config.equal("/tmp/conky.config"):
                config.save();
                config.saveas("/tmp/conky.config");
        except KeyboardInterrupt:
            sys.exit(0);
        except:
            traceback.print_exc();
        finally:
            time.sleep(10);

def rodar():
    p = Process("conky -d -c /tmp/conky.config");
    output = p.run();

time.sleep(1);
t1 = Thread(target=documento)
t1.start();


time.sleep(1);
t2 = Thread(target=rodar)
t2.start()
t2.join();
t1.join();