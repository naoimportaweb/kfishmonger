
from .process import Process;
from .empacotador import _ids;

class Pip():
    def install(self, package):
        # A flag do pip varia por distro. Usamos o ID do os-release (confiável),
        #    não mais o distro.name() antigo (baseado em platform.version()).
        ids = _ids();
        if "ubuntu" in ids:
            p = Process("pip3 install " + package);
        elif ("debian" in ids) or ("kali" in ids):
            p = Process("pip3 install " + package + " --break-system-packages");
        else:
            p = Process("pip3 install " + package + " --root-user-action=ignore");
        p.run();
