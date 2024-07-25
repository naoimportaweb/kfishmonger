import os;

from subprocess import STDOUT, check_call;
from .process import Process;

class Apt:
    def __init__(self, log=None,verbose=False):
        self.log = log;
        self.verbose = verbose;
    
    def update(self):
        check_call(['apt', 'update', '-y'], stdout=open(os.devnull,'wb'), stderr=STDOUT);
        if self.log != None:
            self.log.info("Instalando pacote " + package + " com APT.");
    def install(self, package):
        check_call(['apt', 'install', package, '-y'], stdout=open(os.devnull,'wb'), stderr=STDOUT);
        if self.log != None:
            self.log.info("Instalando pacote " + package + " com APT.");
        if self.verbose:
            print("\t:-) Pacote instalado: ", package);
    
    def exists(self, package):
        p = Process("apt-cache show " + package);
        output = p.run();
        return output.find("E: No packages found") < 0;
    
    def apt_add_repository(self, repo):
        check_call(['apt-add-repository', repo], stdout=open(os.devnull,'wb'), stderr=STDOUT);
        if self.log != None:
            self.log.info("Instalando pacote " + package + " com APT.");
    
    def addrepo(self, repo):
        p = Process("echo \"deb https://deb.debian.org/debian/ "+ repo +" main\" | sudo tee /etc/apt/sources.list.d/"+ repo +".list");
        p.run();
        p = Process("apt update -y");
        p.run();
    
    def instaled(self, package):
        p = Process("dpkg-query -W " + package);
        output = p.run();
        return output.find("no packages found matching") < 0;
    
    def purge(self, package):
        check_call(['apt', 'purge', package, '-y'], stdout=open(os.devnull,'wb'), stderr=STDOUT);