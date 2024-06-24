import sys, os, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.process import Process;

# =========== INICIANDO SERVICOS E PROGRMAS ===============

#contador = 0;
#def retorno(process, s):
#    global contador;
#    contador = contador + 1
#    print( s );
#    if contador > 10:
#        process.kill();
#def main():
#    p = Process("netstat -c --numeric-hosts | grep -e ESTABLISHED | grep -e tcp -e udp");
#    p.asThread(retorno);
#if __name__ == "__main__":
#    main();
def callbakc_retorno(process, ret):
    print(ret);
p = Process("python3 " + CURRENTDIR + "/sub/monitor.py");
p.asThread(callbakc_retorno);

process = Process("/etc/dnscrypt-proxy/linux-x86_64/dnscrypt-proxy -config /etc/dnscrypt-proxy/linux-x86_64/dnscrypt-proxy.toml");
process.run();