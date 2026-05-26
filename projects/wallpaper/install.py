import sys, os, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.config import Config;
from api.downloadinstall import DownloadInstall;

def main():
    if not os.path.exists("/var/kfm/wallpeper"):
        os.makedirs("/var/kfm/wallpeper");
    down = DownloadInstall("kfmwallpaper.zip", "https://codeload.github.com/naoimportaweb/kfmwallpaper/zip/refs/heads/main");
    down.download();
    down.extract("/tmp/wallpaper/kfmwallpaper-main");

if __name__ == "__main__":
    main();

