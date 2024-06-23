
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

    def exclude14eyes(self):
        if self.findattribute("ExcludeNodes") == None:
            self.addattribute("ExcludeNodes {us},{uk},{gb},{ca},{il},{nl},{no},{dk},{au},{nz},{fr},{de},{be},{se},{es},{it}");
        if self.findattribute("ExcludeExitNodes") == None:
            self.addattribute("ExcludeExitNodes {us},{uk},{gb},{ca},{il},{nl},{no},{dk},{au},{nz},{fr},{de},{be},{se},{es},{it}");     
        if self.findattribute("StrictNodes") == None:
            self.addattribute("StrictNodes 1");
def main():
    t = Torrc();
    t.runasdaemon();
    t.tunnelport(9051);
    t.exclude14eyes();
    t.save();
if __name__ == "__main__":
    main();


#14eyes
#StrictNodes 1
#ExcludeNodes {us},{gb},{ca},{nz},{au},{dk},{fr},{nl},{no},{de},{be},{es},{it},{se}
#ExcludeExitNodes {us},{gb},{ca},{nz},{au},{dk},{fr},{nl},{no},{de},{be},{es},{it},{se}
