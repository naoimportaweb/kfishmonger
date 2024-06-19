
from .process import Process;
from .distro import Distro;
class Pip():
    def install(self, package):
        distro = Distro();
        p = Process("pip3 install " + package + " --root-user-action=ignore");
        #if distro.name == "debian":
        #    p = Process("pip3 install " + package + " --break-system-packages");
        p.run();


