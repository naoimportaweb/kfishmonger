import sys, os, shutil, time, hashlib, netifaces, json, traceback

sys.path.insert(0,"/opt/kfishmonger/projects/") 

from threading import Thread
from api.process import Process;
from api.config import Config;
from api.distro import Distro;

def md5(path):
    if not os.path.exists(path):
        return "";
    return hashlib.md5( open( path, "r" ).read().encode() ).hexdigest()

def documento():
    while True:
        try:
            shutil.copy( "/opt/kfishmonger/projects/conky/resources/conky.config", "/tmp/conky.buffer.config");
            p = Process("chmod 666 /tmp/conky.buffer.config");
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
            config.saveas("/tmp/conky.buffer.config");
            if not os.path.exists("/tmp/conky.config") or md5("/tmp/conky.config") != md5("/tmp/conky.buffer.config"):
                config.saveas("/tmp/conky.config");
                p = Process("chmod 666 /tmp/conky.config");
                p.run();
        except KeyboardInterrupt:
            sys.exit(0);
        except:
            traceback.print_exc();
        finally:
            time.sleep(10);

def rodar():
    p = Process("conky -q -d -c /tmp/conky.config");
    output = p.run();

if os.path.exists("/tmp/conky.config"):
    os.unlink("/tmp/conky.config");
if os.path.exists("/tmp/conky.buffer.config"):
    os.unlink("/tmp/conky.buffer.config");

time.sleep(1);
t1 = Thread(target=documento)
t1.start();

time.sleep(1);
t2 = Thread(target=rodar)
t2.start()
t2.join();
t1.join();