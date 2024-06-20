import sys, os, shutil, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.apt import Apt;
from api.config import Config;

def main():
    apt = Apt();
    apt.install("proxychains");
    config = Config("/etc/proxychains.conf");
    config.open()
    config.uncomment("proxy_dns");
    config.uncomment("dynamic_chain");
    config.commentattr("strict_chain");
    config.commentattr("socks4");
    if config.findattribute("socks5") == None:
        config.addattribute( "socks5 127.0.0.1 9050" );
    config.save();

if __name__ == "__main__":
    main();

