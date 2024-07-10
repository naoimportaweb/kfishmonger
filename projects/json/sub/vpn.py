#!/usr/bin/python3

import socket, json, requests;
import sys, os, shutil, inspect, time;
import re

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR));
sys.path.append(ROOT);

from api.systemctl import Systemctl

HOST = "127.0.0.1";
PORT = 20000;

s = Systemctl("vpn.service");
if s.running():
    r = requests.get("https://wtfismyip.com/json");
    js_myip = json.loads(r.text);
else:
    js_myip = {"YourFuckingCountry" : "-", "YourFuckingIPAddress" : "-"}
    print("VPN Service desativado no Systemctl");

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT));
    js = {"vpn" : {"country" : js_myip["YourFuckingCountry"], "ip" : js_myip["YourFuckingIPAddress"] }};
    dados = "00000000000000000000" + json.dumps(js);
    s.sendall( dados.encode() );

