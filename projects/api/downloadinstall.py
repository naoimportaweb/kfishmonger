import uuid, stat;
import sys, os, shutil, inspect, time, hashlib;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);
sys.path.append(CURRENTDIR);

from api.process import Process;

class DownloadInstall():
    def __init__(self, file, url, hash_file=None, log=None):
        self.url = url;
        self.file = file;
        self.hash_file = hash_file;
        self.tmp = "/tmp/" + str(uuid.uuid4());
        os.makedirs(self.tmp);
    
    def getPath(self):
        return "/tmp/" + self.file;

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

    def download(self, force=True):
        # aqui é para baixar o arquivbo
        if os.path.exists( self.getPath()) and force == True:
            os.unlink(self.getPath());
        if not os.path.exists(self.getPath()):
            process = Process("wget "+ self.url +" -O " + self.getPath());
            process.run();
        
        # faz validacao caso exista uma hash de validaçao
        if self.hash_file != None:
            if not hashlib.sha256( open(  self.getPath() , "rb").read() ).hexdigest() == self.hash_file:
                raise Exception("A hash do arquivo não confere.");
        
        # Descompactar os tipos de arquivos
        # TODO: tem que melhorar fazer uma reflexaáo de codigo e reduzir numero de linahs nos ifs a baixo
        if self.file.find("tar.gz") > 0:
            process = Process("tar xzvf " + self.getPath() + " -C "+ self.tmp +" --strip-components 1");
            process.run();
        elif self.file.find(".zip") > 0:
            process = Process("unzip " + self.getPath() + " -d "+ self.tmp +"");
            process.run();
        elif self.file.find("tar.bz2") > 0:
            process = Process("tar -xjvf "+ self.getPath() +" -C "+ self.tmp  +" --strip-components 1");
            process.run();
        else:
            process = Process("tar --strip-components 1 -C "+ self.tmp +" -xf " + self.getPath());
            process.run();
        return self.tmp;

    def extract(self, path, permission=True):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True);
        shutil.copytree(self.tmp, path , dirs_exist_ok=True)
        if permission == True:
            self.__permission__(path);
    
    def make(self):
        self.download();
        process = Process("make -C " + self.tmp);
        process.run(); 
        process = Process("make -C " + self.tmp + " install");
        process.run(); 