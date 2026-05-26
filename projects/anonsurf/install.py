import os, sys, platform, shutil, inspect, getpass, stat;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.log import Log;
from api.config_project import ConfigProject

log = Log("anonsurf");
config_project = ConfigProject("anonsurf", log=log);
config_project.copy();

def main():
    os.symlink("/opt/kfishmonger/projects/anonsurf/resources/anonsurf.sh", "/bin/anonsurf")
    st = os.stat('/opt/kfishmonger/projects/anonsurf/resources/anonsurf.sh')
    os.chmod('/opt/kfishmonger/projects/anonsurf/resources/anonsurf.sh', st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
if __name__ == "__main__":
    main();