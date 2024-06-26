import uuid;
import sys, os, shutil, inspect, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);
sys.path.append(CURRENTDIR);

from api.process import Process;

class DownloadInstall():
    def __init__(self, path, file, url):
        self.path = path;
        self.url = url;
        self.file = file;
        self.tmp = "/tmp/" + str(uuid.uuid4());
        os.makedirs(self.tmp);

    def download(self):
        if os.path.exists("/tmp/" + self.file):
            os.unlink("/tmp/" + self.file);
        process = Process("wget "+ self.url +" -O /tmp/" + self.file);
        process.run();
        process = Process("tar --strip-components 1 -C "+ self.tmp +" -xf /tmp/" + self.file);
        process.run(); 
    
    def make(self):
        self.download();
        process = Process("make -C " + self.tmp);
        process.run(); 
        process = Process("make -C " + self.tmp + " install");
        process.run(); 