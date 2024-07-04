import sys, os, inspect, traceback, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.process import Process;
from api.resolv import Resolv
# =========== INICIANDO SERVICOS E PROGRMAS ===============

while True:
    try:
        process = Process("/etc/dnscrypt-proxy/linux-x86_64/dnscrypt-proxy -config /etc/dnscrypt-proxy/linux-x86_64/dnscrypt-proxy.toml");
        if not process.exists():
            process.run();
        else:
            print("Processo em execucao.");
    except KeyboardInterrupt:
        sys.exit(0);
    except:
        traceback.print_exc();
    time.sleep(60);