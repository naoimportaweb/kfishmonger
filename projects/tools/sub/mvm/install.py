import sys, os, shutil, inspect;
import requests, shutil;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENTDIR)));
sys.path.append(ROOT);

from api.empacotador import Empacotador;
from api.downloadinstall import DownloadInstall

def main():    
    empacotador = Empacotador.detectar(verbose=True);
    empacotador.install("ffmpeg");
    empacotador.install("qtmultimedia5-dev");
    empacotador.install("libcurl4-openssl-dev");
    empacotador.install("libjsoncpp-dev");
    empacotador.install("libopencv-dev");
    empacotador.install("libqt5multimedia5-plugins");

    if not os.path.exists("/tmp/mvm"):
        os.makedirs("/tmp/mvm");
    if not os.path.exists("/opt/mvm"):
        os.makedirs("/opt/mvm");
    if not os.path.exists("/opt/mvm/bin"):
        os.makedirs("/opt/mvm/bin");
    
    down = DownloadInstall("mvm.tar.gz", "https://sourceforge.net/projects/multilanguage-video-maker/files/latest/download");
    down.download(force=True);
    down.extract("/tmp/mvm/");
    
    shutil.copy("/tmp/mvm/bin/video", "/opt/mvm/bin/");
    if not os.path.exists("/bin/mvm"):
        os.symlink("/opt/mvm/bin/video", "/bin/mvm");
if __name__ == "__main__":
    main();


