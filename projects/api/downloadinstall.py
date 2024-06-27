import uuid, stat;
import sys, os, shutil, inspect, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);
sys.path.append(CURRENTDIR);

from api.process import Process;

class DownloadInstall():
    def __init__(self, file, url):
        self.url = url;
        self.file = file;
        self.tmp = "/tmp/" + str(uuid.uuid4());
        os.makedirs(self.tmp);

    def __permission__(self, path):
        if not os.path.exists(path):
            return;
        if os.path.isdir(path):
            os.chmod(path, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH);
            lista = os.listdir( path );
            for item in lista:
                self.__permission__(path + "/" + item);
        else:
            st = os.stat(path);
            if  bool(st.st_mode & stat.S_IEXEC):
                os.chmod(path, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH);
            else:
                os.chmod(path, st.st_mode | stat.S_IRGRP | stat.S_IROTH);

    def download(self):
        if os.path.exists("/tmp/" + self.file):
            os.unlink("/tmp/" + self.file);
        process = Process("wget "+ self.url +" -O /tmp/" + self.file);
        process.run();
        if self.file.find("tar.gz"):
            #p = Process("tar xzvf "+ path +" -C /opt/ggh/ --strip-components=1");
            process = Process("tar xzvf /tmp/" + self.file + " -C "+ self.tmp +" --strip-components 1");
            process.run();
        else:
            process = Process("tar --strip-components 1 -C "+ self.tmp +" -xf /tmp/" + self.file);
            process.run();

    def extract(self, path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True);
        shutil.copytree(self.tmp, path , dirs_exist_ok=True)
        self.__permission__(path);
    
    def make(self):
        self.download();
        process = Process("make -C " + self.tmp);
        process.run(); 
        process = Process("make -C " + self.tmp + " install");
        process.run(); 