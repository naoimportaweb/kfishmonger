
from .process import Process;
from .distro import Distro;
class Pip():
    def install(self, package):
        distro = Distro();
        print("DISTRO NAME", distro.name());
        
        if distro.name() == "debian":
            p = Process("pip3 install " + package + " --break-system-packages");
        elif distro.name() == "ubuntu":
            p = Process("pip3 install " + package );
        else:
            p = Process("pip3 install " + package + " --root-user-action=ignore");
        p.run();


