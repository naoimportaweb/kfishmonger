import sys, os, shutil, inspect, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.process import Process;

process = Process("dig ubuntu.com @127.0.2.1");
print(process.run());

process = Process("nslookup ubuntu.com");
print(process.run());

