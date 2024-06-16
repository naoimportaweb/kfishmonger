import sys, os, shutil;
sys.path.insert(0,"/opt/kfishmonger/projects/") 

print(sys.path);
from api.process import Process;

p = Process("conky -d -c /opt/kfishmonger/projects/conky/debian/xfce/resources/conky.config");
output = p.run();

for linha in output:
    print(linha);


