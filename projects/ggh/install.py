import sys, os, shutil, inspect;
import requests, shutil;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.config import Config;
from api.pip import Pip;
from api.process import Process;

def download_file(url, local_filename):
    if os.path.exists( local_filename ):
        os.unlink( local_filename );
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            return True;
    return False;

def main():    
    pip = Pip();
    pip.install("xmpppy");
    pip.install("PySide6");
    pip.install("pycryptodome");

    if not os.path.exists("/opt/ggh"):
        os.makedirs("/opt/ggh");
    if os.path.exists("/bin/ggh"):
        os.unlink("/bin/ggh");
    url = "https://sourceforge.net/projects/ggh/files/latest/download";
    path = "/tmp/ggh.tar.gz";
    download_file(url, path);
    p = Process("tar xzvf "+ path +" -C /opt/ggh/ --strip-components=1");
    p.run();
    p = Process("chmod +x /opt/ggh/cliente/app.py");
    p.run();
    os.symlink("/opt/ggh/client/app.py", "/bin/ggh")

if __name__ == "__main__":
    main();






