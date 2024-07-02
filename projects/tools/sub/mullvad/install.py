import sys, os, shutil, inspect, time, getpass;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENTDIR)));
sys.path.append(ROOT);

from api.downloadinstall import DownloadInstall;
from api.process import Process;
from api.distro import Distro

distro = Distro();

def main():
    download = DownloadInstall("mullvadbrowser.tar.xz","https://mullvad.net/pt/download/browser/linux-x86_64/latest");
    download.download();
    download.extract("/opt/mullvad/");

    if not os.path.exists("/home/"+ distro.user()  +"/.local/share/applications"):
        os.makedirs("/home/"+ distro.user()  +"/.local/share/applications");
    
    shutil.copy( CURRENTDIR + "/resources/mullvad.desktop", "/home/"+ distro.user()  +"/.local/share/applications");
    shutil.copy( CURRENTDIR + "/resources/mullvad-proxy.desktop", "/home/"+ distro.user()  +"/.local/share/applications");

    process = Process("chown -R " + distro.user() + " /opt/mullvad");
    process.run();
    process = Process("chown -R " + distro.user() + ":"+ distro.user() +" /home/"+ distro.user()  +"/.local/share/applications/mullvad.desktop");
    process.run();
    process = Process("chown -R " + distro.user() + ":"+ distro.user() +" /home/"+ distro.user()  +"/.local/share/applications/mullvad-proxy.desktop");
    process.run();
    process = Process("xdg-settings set default-web-browser mullvad.desktop"); #set default browser mullvad
    process.run();

if __name__ == "__main__":
    main();

#https://mullvad.net/pt/download/browser/linux