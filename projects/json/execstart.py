import socket, os, sys, json, traceback, inspect, shutil, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname( CURRENTDIR );
sys.path.append(ROOT);

from api.process import Process;
from threading import Thread;

BLOCO = 1024;
PATH_JSON="/tmp/fishmonger.json";

# Iniciando o arquivo JSON
shutil.copy(CURRENTDIR + "/resources/base.json", PATH_JSON);
js = json.loads(open( PATH_JSON ).read());

def processar_requisicao(addr, conn):
    data = conn.recv(40960);
    versao = data[:20];
    data = json.loads(data[20:]);
    return versao000000001(data);

def joinJson(js1, js2):
    for key in js2.keys():
        if type(js2[key]).__name__ == "dict":
            if js1 == None:
                return;
            if js1.get(key) == None:
                js1[key] = {};
            js1 = joinJson(js1[key], js2[key]);
        else:
            js1[key] = js2[key];

def versao000000001(data):
    global js;
    joinJson(js, data);
    return True;

def persist():
    global js, PATH_JSON;
    while True:
        try:
            with open(PATH_JSON, "w") as f:
                f.write(json.dumps( js ));
        except:
            traceback.print_exc();
        finally:
            time.sleep(5);
def monitor():
    p = Process( "python3 " + CURRENTDIR + "/monitor.py" );
    p.run();

def main():
    global js;
    tpersist = Thread(target=persist);
    tpersist.start();

    tmonitor = Thread(target=monitor);
    tmonitor.start();
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Service fishmonger.json started, port: 20000");
        s.bind(("", 20000));
        s.listen(100);
        while True:
            try:  
                conn, addr = s.accept();
                print("Endereco:", addr);
                t = Thread(target=processar_requisicao, args=(addr, conn, ));
                t.start();
            except KeyboardInterrupt:
               sys.exit(1);
            except:
               traceback.print_exc();
if __name__ == '__main__':
    main();
