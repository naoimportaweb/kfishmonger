import os;
import subprocess;

class Process:
    def __init__(self, command):
        self.textual = command;
        self.comand = command.split(" ");
    def exists(self):
        #ps aux | grep -v grep | grep
        commando = "ps aux";
        print(commando.split(" "));
        p = subprocess.Popen(commando.split(" "), stdout=subprocess.PIPE, universal_newlines=True);
        return p.stdout.read().find( self.textual ) > 0;
    def run(self):
        p = subprocess.Popen(self.comand, stdout=subprocess.PIPE, universal_newlines=True);
        #for linha in p.stdout:
        #    print(linha);
        return p.stdout;