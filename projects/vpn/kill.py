import sys, os, shutil, inspect, getpass, json;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.log import Log;
from vpn.api.routers import Routers;
from api.config_project import ConfigProject;

routers = Routers();
log = Log("vpn");
log.info("Ligando o kill");
config = ConfigProject("vpn", log=log);
config.load();

#path_configuracao = "/var/kfm/vpn/config.json";
#json_config = {};
#if os.path.exists(path_configuracao):
#    json_config = json.loads( open(path_configuracao).read() );

if config.kill == True:
    if config.gateway != None:
        routers.kill( config.gateway );
        log.info("Removido a regra default.");
    else:
        log.error("Nao foi possivel, voce deve configurar um Gateway. Conforme documentacao oficial.");
else:
    log.error("Nao foi possivel, voce deve configurar a chave kill com valor true. Conforme documentacao oficial.");
