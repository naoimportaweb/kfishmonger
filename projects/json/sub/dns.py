import sys, os, inspect, json;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR));
sys.path.append(ROOT);
sys.path.append(ROOT + "/json/");

from api.systemctl import Systemctl;
from api.jsonclient import JsonClient;

ip = "-";
with open("/etc/resolv.conf", "r") as r:
    lines = r.readlines();
    for line in lines:
        if line.strip()[:len("nameserver ")] == "nameserver ":
            part = line.strip().split(" ");
            ip = part[1];
            break;

jsonclient = JsonClient();
jsonclient.send( {"dns" : {"ip" : ip }} );


