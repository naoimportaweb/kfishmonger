import socket, os, sys, json, traceback, inspect, shutil, time, re;

# Sempre que o serviço for iniciado ele roda o execstart.py, se quiser ver dcomo é
#    veja em resources/kfm_network.service
# Aqui faz o que tem que ser feito....

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname( CURRENTDIR );
sys.path.append(ROOT);

from api.process import Process;

def callbakc_retorno(process, ret):
    print(ret);

def main():
    p = Process("python3 " + CURRENTDIR + "/sub/dns_monitor.py");
    p.asThread(callbakc_retorno);

if __name__ == '__main__':
    main();
