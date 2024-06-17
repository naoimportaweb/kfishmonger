import sys, os, shutil;
sys.path.insert(0,"/opt/kfishmonger/projects/") 

print(sys.path);
from api.process import Process;
from api.config import Config;
from api.distro import Distro;

shutil.copy( "/opt/kfishmonger/projects/conky/ubuntu/gnome/resources/conky.config", "/tmp/conky.config");
distro = Distro();
config = Config("/tmp/conky.config");
config.open();
config.replace("{INTERFACE}", distro.interfaces()[1]);
config.save();

p = Process("conky -d -c /tmp/conky.config");
output = p.run();

for linha in output:
    print(linha);


