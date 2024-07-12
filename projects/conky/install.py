import os, sys, platform, shutil, inspect, getpass;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.distro import Distro;
from api.process import Process;
from api.log import Log;
from api.config_project import ConfigProject;

log = Log("conky");
config_project = ConfigProject("conky", log=log);
config_project.copy();

def main():
    # FIND BY INSTALL SCRIPT
    distro = Distro();
    path_script = CURRENTDIR + "/" + distro.name() + "/install.py";
    if not os.path.exists(path_script):
        path_script = CURRENTDIR + "/" + distro.name() + "/" + distro.graphical() + "/install.py";
    
    # RUN INSTALL SCRIPT
    process = Process("python3 " + path_script);
    process.run();
    process = Process("chown -R " + distro.user() + ":" + distro.user() + " /opt/kfishmonger");
    process.run();

if __name__ == "__main__":
    main();