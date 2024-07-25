import sys, os, shutil, inspect;
import requests, shutil;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENTDIR)));
sys.path.append(ROOT);

from api.apt import Apt;
from api.downloadinstall import DownloadInstall


def main():    
    apt = Apt();
    apt.install("ffmpeg");
    apt.install("qtmultimedia5-dev");
    apt.install("libcurl4-openssl-dev");
    apt.install("libjsoncpp-dev");
    apt.install("libopencv-dev");
    apt.install("libqt5multimedia5-plugins");

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


