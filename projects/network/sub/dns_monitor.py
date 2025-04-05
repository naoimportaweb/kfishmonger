import sys, os, shutil, inspect, time, traceback, time;

# Chamado no command line exemplo: sudo kfm -p dns -c install -s dns_monitor
#    ai esse script vem e atua no serviço, neste caso pedindo um dns_monitor


CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR));
sys.path.append(ROOT);
sys.path.append(ROOT + "/dns/");

from api.resolv import Resolv;
from api.dig import Dig;
from api.CONST import *

time.sleep(60);

while True:
    try:
        d = Dig("ubuntu.com");
        r = Resolv();
        r.clear();
        r.add("# não editar");
        if d.ip() == None:
            r.add("nameserver " + DNS_DEFAULT_RESOLVER);
        else:
            #nameserver 127.0.2.1 no resolv.conf
            r.add("nameserver 127.0.2.1");
        r.save();
        r.block();
    except KeyboardInterrupt:
        sys.exit(0);
    except:
        traceback.print_exc();
    finally:
        time.sleep(30);
