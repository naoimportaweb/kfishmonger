import sys, os, shutil, inspect;
import requests, shutil, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENTDIR)));
sys.path.append(ROOT);

from api.empacotador import Empacotador;
from api.config import Config;
from api.pip import Pip;
from api.process import Process;
from api.distro import Distro
from api.downloadinstall import DownloadInstall

def download_file(url, local_filename):
    if os.path.exists( local_filename ):
        os.unlink( local_filename );
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            return True;
    return False;

def main():    
    empacotador = Empacotador.detectar();
    distro = Distro();
    pip = Pip();
    url = "https://codeload.github.com/naoimportaweb/codoenc/zip/refs/heads/main";
    path = "/tmp/codoencrypt.zip";
    download_file(url, path);
    os.system("unzip -o -qq /tmp/codoencrypt.zip -d /tmp/ && cp -r /tmp/codoenc-main/* /opt/codoencrypt/ && cd /opt/codoencrypt/ && /bin/bash ./app/install.sh && /bin/bash ./local/install.sh");
    shutil.copy( CURRENTDIR + "/resources/codo.desktop", "/home/"+ distro.user()  +"/.local/share/applications");
    process = Process("chown -R " + distro.user() + ":"+ distro.user() +" /home/"+ distro.user()  +"/.local/share/applications/codo.desktop");
    process.run();

if __name__ == "__main__":
    main();



