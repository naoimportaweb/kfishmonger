import sys, os, inspect, traceback, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.log import Log;
from api.process import Process;
from api.resolv import Resolv;
from api.config import Config;
from api.config_project import ConfigProject;
from api.CONST import *;

# =========== INICIANDO SERVICOS E PROGRMAS ===============

log = Log("dns");
config_project = ConfigProject("dns", log=log);
config_project.load();

# sempre qué é executado,o script monta o arquivo de configuração TOML
config_user = Config( PATH_SYSTEM + "/projects/dns/resources/dnscrypt-proxy.toml" );
config_user.open();
#config_user.replace("TOR_SOCKS_5", "socks5://127.0.0.1:" + str(TOR_SOCKS_5_PORT));
config_user.replace("TOR_SOCKS_5", "");
config_user.replace("SERVER_NAME", config_project.server_name);
config_user.replace("DNS_LISTEN_PORT", DNS_LISTEN_PORT);
config_user.saveas("/etc/dnscrypt-proxy/linux-x86_64/dnscrypt-proxy.toml");

if config_project.execute:
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