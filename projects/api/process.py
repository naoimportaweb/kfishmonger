import os;
import subprocess;
import psutil

class Process:
    def __init__(self, command, wait=True):
        self.textual = command;
        self.comand = command.split(" ");
        self.wait = wait;
        self.p = None;
    
    def exists(self):
        #ps aux | grep -v grep | grep
        commando = "ps aux";
        print(commando.split(" "));
        self.p = subprocess.Popen(commando.split(" "), stdout=subprocess.PIPE, universal_newlines=True);
        return self.p.stdout.read().find( self.textual ) > 0;
    
    def run(self):
        self.p = subprocess.Popen(self.comand, stdout=subprocess.PIPE, universal_newlines=True);
        (output, err) = self.p.communicate();
        if self.wait:
            p_status = self.p.wait();
        return output;
    
    def stopProcess(self):
        self.p.kill();

    def kill(self):
        for proc in psutil.process_iter():
            if proc.name().find(self.textual) >= 0:
                try:
                    proc.kill();
                except:
                    print(".");
            for command in proc.cmdline():
                if command.find(self.textual) >= 0:
                    try:
                        proc.kill();
                        break;
                    except:
                        print(".");
                    