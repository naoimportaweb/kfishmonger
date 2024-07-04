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

ip = "-";
with open("/etc/resolv.conf", "r") as r:
    lines = r.readlines();
    for line in lines:
        if line.strip()[:len("nameserver ")] == "nameserver ":
            part = line.strip().split(" ");
            ip = part[1];
            break;

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT));
    js = {"dns" : {"ip" : ip }};
    dados = "00000000000000000000" + json.dumps(js);
    s.sendall( dados.encode() );

