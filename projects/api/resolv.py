import sys, os, shutil, inspect, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);
sys.path.append(CURRENTDIR);

from api.config import Config;

class Resolv(Config):
    def __init__(self):
        super().__init__("/etc/resolv.conf");
        
def main():
    r = Resolv();
    r.clear();
    r.add("nameserver 127.0.2.1");
    r.save();
    r.block();

if __name__ == "__main__":
    main();