
from .config import Config;

class Torrc(Config):
    def __init__(self):
        super().__init__("/etc/tor/torrc");
        self.open();

    def runasdaemon(self):
        if self.findattribute("RunAsDaemon") == None:
            self.addattribute("RunAsDaemon 1");

    def tunnelport(self, port):
        if self.findattribute("HTTPTunnelPort") == None:
            self.addattribute("HTTPTunnelPort " + str(port));

def main():
    t = Torrc();
    t.runasdaemon();
    t.tunnelport(9051);
    t.save();
if __name__ == "__main__":
    main();