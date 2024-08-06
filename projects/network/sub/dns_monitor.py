import sys, os, shutil, inspect, time, traceback, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR));
sys.path.append(ROOT);
sys.path.append(ROOT + "/dns/");

from api.resolv import Resolv;
from api.dig import Dig;

time.sleep(60);

while True:
    try:
        d = Dig("ubuntu.com");
        r = Resolv();
        r.clear();
        r.add("# não editar");
        if d.ip() == None:
            #nameserver 1.1.1.1 no resolv.conf
            r.add("nameserver 1.1.1.1");
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
