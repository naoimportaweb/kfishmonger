import os;
import subprocess;

class Process:
    def __init__(self, command):
        self.comand = command.split(" ");

    def run(self):
        p = subprocess.Popen(self.comand, stdout=subprocess.PIPE, universal_newlines=True);
        return p.stdout;