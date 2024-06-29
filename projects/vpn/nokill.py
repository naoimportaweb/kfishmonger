import sys, os, shutil, inspect, getpass, json;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);


from vpn.api.routers import Routers;

routers = Routers();

path_configuracao = "/var/kfm/vpn/config.json";
json_config = {};
if os.path.exists(path_configuracao):
    json_config = json.loads( open(path_configuracao).read() );

if json_config.get("kill") == True:
    if json_config.get("gateway") != None:
        routers.deskill(json_config["gateway"]);
    else:
        print("Nao foi possivel, voce deve configurar um Gateway. Conforme documentacao oficial.");
else:
    print("Nao foi possivel, voce deve configurar a chave kill com valor true. Conforme documentacao oficial.");
