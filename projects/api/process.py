import os;
import subprocess, signal;
import psutil, time;

from threading import Thread

class Process:
    def __init__(self, command, wait=True):
        self.textual = command;
        self.comand = command.split(" ");
        self.wait = wait;
        self.p = None;
        self.th = None;
        self.stop_thread = False;
    
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
        if self.th != None:
            self.stop_thread = True;
    
    def __asThread__(self, callback):
        self.p = subprocess.Popen(self.textual, shell=True, stdout=subprocess.PIPE);
        while True:
            line = self.p.stdout.readline();
            if line == None or self.stop_thread:
                break;
            line = line.decode().strip();
            if line == "":
                time.sleep(0.1);
                continue;
            callback(self, line );

    def asThread(self, callback):
        self.th = Thread(target=self.__asThread__, args=(callback,));
        self.th.start();

#contador = 0;
#def retorno(process, s):
#    global contador;
#    contador = contador + 1
#    print( s );
#    if contador > 10:
#        process.kill();
#def main():
#    p = Process("netstat -c --numeric-hosts | grep -e ESTABLISHED | grep -e tcp -e udp");
#    p.asThread(retorno);
#if __name__ == "__main__":
#    main();

