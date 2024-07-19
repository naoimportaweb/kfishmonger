import socks, socket, json, sys, os, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR));
sys.path.append(ROOT);
sys.path.append(ROOT + "/json/");

from urllib import request;
from api.jsonclient import JsonClient;

_socket = socket.socket
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket
r = request.urlopen('https://wtfismyip.com/json')
js_myip = json.loads(r.read());

# Tem que voltar o socket sem o proxy
socket.socket = _socket

jsonclient = JsonClient();
jsonclient.send( {"tor" : {"country" : js_myip["YourFuckingCountry"], "ip" : js_myip["YourFuckingIPAddress"] }} );
