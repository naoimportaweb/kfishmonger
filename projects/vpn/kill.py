import sys, os, shutil, inspect, getpass, json;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.log import Log;
from vpn.api.routers import Routers;

routers = Routers();
log = Log("vpn");
log.info("Ligando o kill");

path_configuracao = "/var/kfm/vpn/config.json";
json_config = {};
if os.path.exists(path_configuracao):
    json_config = json.loads( open(path_configuracao).read() );

if json_config.get("kill") == True:
    if json_config.get("gateway") != None:
        routers.kill(json_config["gateway"]);
        log.info("Removido a regra default.");
    else:
        print("Nao foi possivel, voce deve configurar um Gateway. Conforme documentacao oficial.");
        log.error("Nao foi possivel, voce deve configurar um Gateway. Conforme documentacao oficial.");
else:
    print("Nao foi possivel, voce deve configurar a chave kill com valor true. Conforme documentacao oficial.");
    log.error("Nao foi possivel, voce deve configurar a chave kill com valor true. Conforme documentacao oficial.");
