import os;
import subprocess;

from .process import Process;

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
                return True;
        return False;

def main():
    sysctl = Systemctl("json.service");
    print( sysctl.exists() );

if __name__ == "__main__":
    main();