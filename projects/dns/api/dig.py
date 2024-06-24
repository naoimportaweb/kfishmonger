import sys, os, shutil, inspect, time;
import re

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR));
sys.path.append(ROOT);

from api.process import Process

class Dig(Process):
    def __init__(self, domain, dns_ip="127.0.2.1"):
        super().__init__("dig "+ domain +" @" + dns_ip);
    def ip(self):
        output = self.run();
        # PRIMEIRO tem que achar exatamente a linha de retorno do dig com a resposta
        reg = "[a-z.]+[\t]+[0-9]+[\t]+[A-Z]+[\t]+[A-Z]+[\t]+[0-9]+.[0-9]+.[0-9]+.[0-9]+";
        retorno_dig = re.search(reg, output);
        if retorno_dig == None:
            return None;
        # SEGUNDO dentro da linha de retorno do DIG, tem que achar o IP
        reg = "[0-9]+.[0-9]+.[0-9]+.[0-9]+";
        retorno_ip = re.search(reg, str(retorno_dig.group()));
        return retorno_ip.group();

def main():
    d = Dig("ubuntu.com");
    print( d.ip() );

if __name__ == "__main__":
    main();