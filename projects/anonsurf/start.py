import sys, os, shutil, time, hashlib, netifaces, json, traceback

sys.path.insert(0,"/opt/kfishmonger/projects/");

from api.process import Process;

p = Process("anonsurf", wait=False);
print( p.run() );
