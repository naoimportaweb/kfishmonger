import sys, os, inspect, traceback, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.log import Log;
from api.process import Process;
from api.resolv import Resolv;
from api.config_project import ConfigProject;
# =========== INICIANDO SERVICOS E PROGRMAS ===============

log = Log("dns");
config = ConfigProject("dns", log=log);
config.load();
if config.execute:
    while True:
        try:
            process = Process("/etc/dnscrypt-proxy/linux-x86_64/dnscrypt-proxy -config /etc/dnscrypt-proxy/linux-x86_64/dnscrypt-proxy.toml");
            if not process.exists():
                log.info("Será iniciado o serviço: /etc/dnscrypt-proxy/linux-x86_64/dnscrypt-proxy");
                process.run();
            else:
                log.info("Já está em execução.");
                print("Processo em execucao.");
        except KeyboardInterrupt:
            sys.exit(0);
        except:
            traceback.print_exc();
        time.sleep(60);
else:
    log.info("A execução do DNS está desabilitado. Consulte o manual.");