import sys, os, shutil, time, hashlib, netifaces, json, traceback

sys.path.insert(0,"/opt/kfishmonger/projects/") 

#from threading import Thread
from api.process import Process;
#from api.config import Config;
#from api.distro import Distro;


process = Process("ps -ef");
saida = process.run().split("\n");

for linha in saida:
    if linha.find("conky") >= 0:
        buffer_array = [];
        for item in linha.split(" "):
            if item != "":
                buffer_array.append( item );
        print(buffer_array[8]);
        p = Process("kill -9 " + buffer_array[1]);
        p.run();