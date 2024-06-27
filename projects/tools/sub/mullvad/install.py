import sys, os, shutil, inspect, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENTDIR)));
sys.path.append(ROOT);

from api.downloadinstall import DownloadInstall;
from api.process import Process;

def main():
    download = DownloadInstall("muvaldbrowser.tar.xz","https://mullvad.net/pt/download/browser/linux-x86_64/latest");
    download.download();
    download.extract("/opt/mullvad/");

    shutil.copy( CURRENTDIR + "/resources/mullvad.desktop", "/home/"+ os.getlogin()  +"/.local/share/applications");
    shutil.copy( CURRENTDIR + "/resources/mullvad-proxy.desktop", "/home/"+ os.getlogin()  +"/.local/share/applications");

    process = Process("chown -R " + os.getlogin() + " /opt/mullvad");
    process.run();
    process = Process("chown -R " + os.getlogin() + ":"+ os.getlogin() +" /home/"+ os.getlogin()  +"/.local/share/applications/mullvad.desktop");
    process.run();
    process = Process("chown -R " + os.getlogin() + ":"+ os.getlogin() +" /home/"+ os.getlogin()  +"/.local/share/applications/mullvad-proxy.desktop");
    process.run();

if __name__ == "__main__":
    main();

#https://mullvad.net/pt/download/browser/linux