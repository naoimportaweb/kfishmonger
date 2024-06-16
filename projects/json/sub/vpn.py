#!/usr/bin/python3

import socket, json, requests;

HOST = "127.0.0.1";
PORT = 20000;

r = requests.get("https://wtfismyip.com/json");
js_myip = json.loads(r.text);

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT));
    js = {"vpn" : {"country" : js_myip["YourFuckingCountry"], "ip" : js_myip["YourFuckingIPAddress"] }};
    dados = "00000000000000000000" + json.dumps(js);
    s.sendall( dados.encode() );

