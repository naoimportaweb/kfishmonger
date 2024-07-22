import sys, os, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENTDIR)));
sys.path.append(ROOT);

from api.apt import Apt;
from api.downloadinstall import DownloadInstall;
from api.log import Log;
from api.systemctl import Systemctl;

def main():
    if not os.path.exists("/opt/monero"):
        os.makedirs("/opt/monero");
    if not os.path.exists("/opt/monero/block"):
        os.makedirs("/opt/monero/block");
    if not os.path.exists("/opt/monero/bin"):
        os.makedirs("/opt/monero/bin");
    log = Log("monero");
    d = DownloadInstall("monerod.tar.bz2", "https://downloads.getmonero.org/linux64");
    d.download(force=False);
    d.extract("/opt/monero/bin", permission=False);
    shutil.copy( CURRENTDIR + "/resources/monerod.service", "/etc/systemd/system/");
    shutil.copy( CURRENTDIR + "/resources/monerod.conf", "/opt/monero/bin/");
    ctl = Systemctl( "monerod.service" , log=log);
    ctl.reload();
    ctl.start();
    ctl.enable();
    if ctl.status():
        print("Rodando o serviço MoneroD");
    else:
        print("O serviço MoneroD não está ligado.");

if __name__ == "__main__":
    main();