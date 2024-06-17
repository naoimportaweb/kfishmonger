

import socks, socket, json;

from urllib import request

HOST = "127.0.0.1";
PORT = 20000;

_socket = socket.socket
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket
r = request.urlopen('https://wtfismyip.com/json')
js_myip = json.loads(r.read());
print(js_myip);
socket


socket.socket = _socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT));
    js = {"tor" : {"country" : js_myip["YourFuckingCountry"], "ip" : js_myip["YourFuckingIPAddress"] }};
    dados = "00000000000000000000" + json.dumps(js);
    s.sendall( dados.encode() );