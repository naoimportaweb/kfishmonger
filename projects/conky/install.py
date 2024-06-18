import os, sys, platform, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.distro import Distro;
from api.process import Process;

def main():
    # FIND BY INSTALL SCRIPT
    distro = Distro();
    path_script = CURRENTDIR + "/" + distro.name() + "/install.py";
    if not os.path.exists(path_script):
        path_script = CURRENTDIR + "/" + distro.name() + "/" + distro.graphical() + "/install.py";
    
    # RUN INSTALL SCRIPT
    process = Process("python3 " + path_script);
    process.run();
    process = Process("chown -R " + os.getlogin() + ":" + os.getlogin() + " /opt/kfishmonger/projects/conky");
    process.run();


if __name__ == "__main__":
    main();