import os;
import subprocess;

from process import Process;

class Systemctl:
    def __init__(self, service, log=None):
        self.log = log;
        self.service = service;
    def exists(self):
        try:
            subprocess.check_call(['systemctl', 'status', self.service], stdout=open(os.devnull,'wb'), stderr=subprocess.STDOUT);
            return True;
        except:
            return False;

    def reload(self):
        subprocess.check_call(['systemctl', 'daemon-reload'], stdout=open(os.devnull,'wb'), stderr=subprocess.STDOUT);

    def enable(self):
        return self.__generico__("enable")

    def disable(self):
        return self.__generico__("disable")

    def start(self):
        return self.__generico__("start")
    
    def stop(self):
        return self.__generico__("stop")

    def restart(self):
        return self.__generico__("restart")
    
    def exists(self):
        return os.path.exists("/etc/systemd/system/" + self.service);

    def __generico__(self, action):
        subprocess.check_call(['systemctl', action, self.service], stdout=open(os.devnull,'wb'), stderr=subprocess.STDOUT);
        return True;
    
    def status(self):
        p = subprocess.Popen(['systemctl' , "--no-pager", "status", self.service], stdout=subprocess.PIPE, universal_newlines=True);
        output = p.stdout;
        for linha in output:
            if linha.find("Active: active") >= 0:
                if self.log != None:
                    self.log.info("O serviço " + self.service + " está ATIVO.");
                return True;
        return False;
    
    def running(self):
        p = subprocess.Popen(['systemctl' , "--no-pager", "status", self.service], stdout=subprocess.PIPE, universal_newlines=True);
        output = p.stdout;
        for linha in output:
            if linha.find("(running)") >= 0:
                if self.log != None:
                    self.log.info("O serviço " + self.service + " está sendo EXECUTADO.");
                return True;
        return False;


