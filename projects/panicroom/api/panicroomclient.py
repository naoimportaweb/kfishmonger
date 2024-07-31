import socket, json;
import sys, os, inspect

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR));
sys.path.append(ROOT);

from api.CONST import *;

class PanicRoomClient():
    def __init__(self, log=None):
        self.host = "127.0.0.1";
        self.port = PANICROOM_PORT;
        self.log = None;
    def send_alert(self, type_alert, message):
        js = {"command" : "add" ,"type" : type_alert, "message" : message };
        if log != None:
            log.info( "ALERT -> " + message );
        self.send(js);
    def send(self, js):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port));
            dados = "00000000000000000000" + json.dumps(js);
            s.sendall( dados.encode() );


