# estou trabalhando nisso.
#https://www.getmonero.org/downloads/hashes.txt
#https://downloads.getmonero.org/gui/monero-gui-linux-x64-v0.18.3.3.tar.bz2
#                                    monero-gui-linux-x64-v0.18.3.3.tar.bz2
import sys, os, shutil, inspect, requests, re;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENTDIR)));
sys.path.append(ROOT);


from api.downloadinstall import DownloadInstall;
from api.log import Log;
from api.CONST import *
from api.distro import Distro

distro = Distro();

PATH_MONERO_GUI = "/opt/monero-gui";

def main():
    if not os.path.exists(PATH_MONERO_GUI):
        os.makedirs(PATH_MONERO_GUI);
    log = Log("monero");
    page = requests.get("https://www.getmonero.org/downloads/hashes.txt");
    texto = page.text;
    linha = re.findall( r'[a-z0-9]+\s*monero-gui-linux-x64-v[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.tar\.bz2', texto );
    colunas = linha[0].replace("  ", " ").split(" ");
    d = DownloadInstall(colunas[1], "https://downloads.getmonero.org/gui/" + colunas[1], hash_file=colunas[0]);
    d.download(force=False);
    d.extract(PATH_MONERO_GUI, permission=False);
    shutil.copy( CURRENTDIR + "/monero.sh", "/opt/monero-gui/");
    shutil.copy( CURRENTDIR + "/resources/monerogui.desktop", "/home/"+ distro.user()  +"/.local/share/applications");


if __name__ == "__main__":
    main();

