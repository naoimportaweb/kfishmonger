import os;
import subprocess;
#from subprocess import STDOUT, check_call;

class Systemctl:
    def __init__(self, service):
        self.service = service;

    def reload(self):
        subprocess.check_call(['systemctl', 'daemon-reload'], stdout=open(os.devnull,'wb'), stderr=subprocess.STDOUT);

    def enable(self):
        return self.__generico__("enable")

    def start(self):
        return self.__generico__("start")
    
    def stop(self):
        return self.__generico__("stop")
    
    def __generico__(self, action):
        subprocess.check_call(['systemctl', action, self.service], stdout=open(os.devnull,'wb'), stderr=subprocess.STDOUT);
        return True;
    
    def status(self):
        p = subprocess.Popen(['systemctl' , "--no-pager", "status", self.service], stdout=subprocess.PIPE, universal_newlines=True);
        output = p.stdout;
        for linha in output:
            if linha.find("Active: active (running)") >= 0:
                return True;
        return False;