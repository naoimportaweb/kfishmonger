import sys, os, shutil, time, hashlib, netifaces, json, traceback

from api.process import Process;

p = Process("anonsurf", wait=False);
print( p.run() );
