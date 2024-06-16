import os;

from subprocess import STDOUT, check_call;

class Apt:
    def install(self, package):
        check_call(['apt', 'install', package, '-y'], stdout=open(os.devnull,'wb'), stderr=STDOUT) 

