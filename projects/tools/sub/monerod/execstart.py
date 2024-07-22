import sys, os, inspect, traceback, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT =  os.path.dirname( os.path.dirname( os.path.dirname(CURRENTDIR) ) );
print("root", ROOT);
sys.path.append(ROOT);

from api.log import Log;
from api.process import Process;
#from api.resolv import Resolv;
#from api.config import Config;
#from api.config_project import ConfigProject;
from api.CONST import *;

# =========== INICIANDO SERVICOS E PROGRMAS ===============

log = Log("monerod");
while True:
    try:
        process = Process("/opt/monero/bin/monerod --data-dir /opt/monero/block");
        if not process.exists():
            log.info("Será iniciado o serviço: /opt/monero/bin/monerod --data-dir /opt/monero/");
            process.run();
        else:
            log.info("Já está em execução.");
            print("Processo em execucao.");
    except KeyboardInterrupt:
        sys.exit(0);
    except:
        traceback.print_exc();
    time.sleep(60);
