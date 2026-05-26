import sys, os, shutil, inspect;

# Esse arquivo é obiragório no projeto, ele tem a rotina específica
#    de instalação do pacote específico, bibliotecas, arrumar arquivos
#    criar diretorios, alocar arquivos, instalar servicos.

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;                    # Para fazer APT install
from api.systemctl import Systemctl;        # Para manipular servicos
from api.log import Log;                    # Para criar logs em /var/kfm/log/
from api.config_project import ConfigProject # Auxiliar para fazer join de .json que
                                             #   está instalado
from api.CONST import *                     # Um arquivo json cheio de constantes                    

# Sempre seguir esse esquema
# 1 - instalar pacotes
# 2 - Copiar arquiivos e criar diretorios
# 3 - Serviços

log = Log("network");
# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
apt = Apt(log=log);
apt.install("net-tools");   # instalando a biblioteca net-tools

# =========== COPIA DE RESOURCES ==========================
config_project = ConfigProject("network", log=log);
config_project.copy();

shutil.copy( CURRENTDIR + "/resources/" + NETWORK_SERVICE, "/etc/systemd/system/");

# =========== INICIANDO SERVICOS E PROGRMAS ===============
# A idéia é que tudo vire serviço, ai vai desabilitando/habilitando
#    os serviços, vai ter uma interface para isso
#    nesse caso vai rodar o execstart.py
ctl = Systemctl( NETWORK_SERVICE );
ctl.reload();
ctl.start();
ctl.enable();
if ctl.status():
    print("Rodando Network");
else:
    print("Nao está rodando.");