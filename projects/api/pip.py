
from .process import Process;

class Pip():
    def install(self, package):
        p = Process("pip3 install " + package + " --break-system-packages");
        return p.run().read();


