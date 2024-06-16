import os;
import subprocess;

class Process:
    def __init__(self, command):
        self.comand = command.split(" ");

    def run(self):
        #print(self.comand);
        p = subprocess.Popen(self.comand, stdout=subprocess.PIPE, universal_newlines=True);
        #for linha in p.stdout:
        #    print(linha);
        return p.stdout;