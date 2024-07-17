import socket, os, sys, json, traceback, inspect, shutil, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname( CURRENTDIR );
sys.path.append(ROOT);

from api.process import Process;
from threading import Thread;
from api.database import Database;
from api.CONST import *;

databases = {};

def processar_requisicao(addr, conn):
    data = conn.recv(40960);
    versao = data[:20];
    data = json.loads(data[20:]);
    print(data);
    retorno = versao000000001(data);
    conn.sendall( json.dumps(retorno).encode() );

def versao000000001(js):
    if databases.get( js["database"] ) == None:
        databases[ js["database"] ] = Database( js["database"] );
    if js["method"] == "schema":
        return databases[ js["database"] ].schema( js["schema"] );
    elif js["method"] == "select":
        return databases[ js["database"] ].datatable( js["sql"], js["values"] );
    elif js["method"] == "insert" or js["method"] == "update" or js["method"] == "delete":
        return databases[ js["database"] ].execute( js["sql"], js["values"] );
    return None;

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Service Database started, port: " + str(DB_PORT));
        s.bind(("127.0.0.1", DB_PORT));
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
if __name__ == "__main__":
    main();



