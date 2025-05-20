import json, requests, sys, os, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR));
sys.path.append(ROOT);
sys.path.append(ROOT + "/json/");

from api.systemctl import Systemctl
from api.CONST import *
from api.jsonclient import *

s = Systemctl( VPN_SERVICE );
if s.running():
    r = requests.get("https://wtfismyip.com/json");
    js_myip = json.loads(r.text);
else:
    js_myip = {"YourFuckingCountry" : "-", "YourFuckingIPAddress" : "-"}
    print("VPN Service desativado no Systemctl");

jsonclient = JsonClient();
jsonclient.send( {"vpn" : {"country" : js_myip["YourFuckingCountry"], "ip" : js_myip["YourFuckingIPAddress"] }} );
