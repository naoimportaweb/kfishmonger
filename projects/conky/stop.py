import sys, os, shutil, time, hashlib, netifaces, json, traceback

sys.path.insert(0,"/opt/kfishmonger/projects/") 

from api.process import Process;

process = Process("ps -ef");
saida = process.run().split("\n");

for linha in saida:
    if linha.find("conky") >= 0:
        buffer_array = [];
        for item in linha.split(" "):
            if item != "":
                buffer_array.append( item );
        p = Process("kill -9 " + buffer_array[1]);
        print(p.run());