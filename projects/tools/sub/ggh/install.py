import sys, os, shutil, inspect;
import requests, shutil;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENTDIR)));
sys.path.append(ROOT);

from api.apt import Apt;
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
    apt = Apt();
    apt.install("libglu1-mesa-dev");
    apt.install("libx11-xcb-dev");
    apt.install("^libxcb*");

    distro = Distro();
    pip = Pip();
    pip.install("xmpppy");
    pip.install("PySide6");
    pip.install("pycryptodome");
    pip.install("Pillow");

    if not os.path.exists("/opt/ggh"):
        os.makedirs("/opt/ggh");
    if os.path.exists("/bin/ggh"):
        os.unlink("/bin/ggh");
    down = DownloadInstall("ggh.tar.gz", "https://sourceforge.net/projects/ggh/files/latest/download");
    down.download();
    down.extract("/opt/ggh");
    url = "https://sourceforge.net/projects/ggh/files/latest/download";
    path = "/tmp/ggh.tar.gz";
    download_file(url, path);
    p = Process("tar xzvf "+ path +" -C /opt/ggh/ --strip-components=1");
    p.run();
    p = Process("chmod +x /opt/ggh/cliente/app.py");
    p.run();
    os.symlink("/opt/ggh/cliente/app.py", "/bin/ggh")
    if not os.path.exists("/home/"+ distro.user()  +"/.local/share/applications"):
        os.makedirs("/home/"+ distro.user()  +"/.local/share/applications");
    
    shutil.copy( CURRENTDIR + "/resources/ggh.desktop", "/home/"+ distro.user()  +"/.local/share/applications");
    shutil.copy( CURRENTDIR + "/resources/ggh-proxy.desktop", "/home/"+ distro.user()  +"/.local/share/applications");

    process = Process("chown -R " + distro.user() + ":"+ distro.user() +" /home/"+ distro.user()  +"/.local/share/applications/ggh.desktop");
    process.run();
    process = Process("chown -R " + distro.user() + ":"+ distro.user() +" /home/"+ distro.user()  +"/.local/share/applications/ggh-proxy.desktop");
    process.run();


if __name__ == "__main__":
    main();






