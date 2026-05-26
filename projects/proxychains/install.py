import sys, os, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.config import Config;
from api.downloadinstall import DownloadInstall;
from api.log import Log;
from api.config_project import ConfigProject

def main():
    log = Log("proxychains");
    config_project = ConfigProject("proxychains", log=log);
    config_project.copy();
    d = DownloadInstall("arquivo.tar.xz", "https://sourceforge.net/projects/proxychains-ng/files/latest/download");
    log.info("Download de https://sourceforge.net/projects/proxychains-ng/files/latest/download");
    d.make();
    log.info("Make proxychains 4");
    shutil.copy( d.tmp + "/src/proxychains.conf", "/etc/");

    if os.path.exists("/usr/bin/proxychains"):
        os.unlink("/usr/bin/proxychains");
    if os.path.exists("/usr/local/bin/proxychains4"):
        os.symlink("/usr/local/bin/proxychains4", "/usr/bin/proxychains")

    config = Config("/etc/proxychains.conf");
    config.open()
    config.uncomment("proxy_dns");
    config.uncommentline("localnet 127.0.0.0/255.0.0.0");
    config.uncomment("dynamic_chain");
    config.commentattr("strict_chain");
    config.commentattr("socks4");
    if config.findattribute("socks5") == None:
        config.addattribute( "socks5 127.0.0.1 9050" );
    config.save();
    log.info("Arquivo de configuração alterado /etc/proxychains.conf");

if __name__ == "__main__":
    main();

