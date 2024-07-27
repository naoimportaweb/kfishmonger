import socket, os, sys, json, traceback, inspect, shutil, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname( CURRENTDIR );
sys.path.append(ROOT);

from api.process import Process;
from threading import Thread;
from api.CONST import *;

js = None;


def processar_requisicao(addr, conn):
    data = conn.recv(40960);
    versao = data[:20];
    data = json.loads(data[20:]);
    return versao000000001(data);

def posicao(busca):
    global js;
    for i in range(len( js["alert"] )):
        if js["alert"][i]["message"] == busca:
            return i;
    return -1;

def add_alert(data):
    global js;
    pos = posicao( data["message"] );
    if pos < 0:
        js["alert"].insert(0, {"type" : data["type"], "message" : data["message"], "cont" : 1});
    else:
        if js["alert"][pos]["cont"] == "":
            js["alert"][pos]["cont"] = 0;
        js["alert"][pos]["cont"] = js["alert"][pos]["cont"] + 1;
        js["alert"].insert(0, js["alert"].pop( pos ) );
    with open( "/tmp/alert.json", "w") as f:
        f.write( json.dumps( js ) );

def versao000000001(data):
    add_alert(data);
    return True;

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Service KFM PANIC ROOM started, port: " + str( PANICROOM_PORT ));
        s.bind(("127.0.0.1", PANICROOM_PORT));
        s.listen(100);
        while True:
            try:  
                conn, addr = s.accept();
                t = Thread(target=processar_requisicao, args=(addr, conn, ));
                t.start();
            except KeyboardInterrupt:
               sys.exit(1);
            except:
               traceback.print_exc();

if __name__ == '__main__':
    if os.path.exists("/tmp/alert.json"):
        os.unlink("/tmp/alert.json");
    shutil.copy( CURRENTDIR + "/resources/alert.json", "/tmp/");
    js = json.loads( open( "/tmp/alert.json", "r").read() );
    main();
