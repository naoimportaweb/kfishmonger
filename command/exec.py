import os, sys, argparse;
import json, shutil, inspect;

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))));
sys.path.append(ROOT + "/projects/");

from api.process import Process;

def main():
    command = "";
    if os.path.exists("/usr/local/bin/proxychains4"):
        command = "proxychains4";
    for i in range(len(sys.argv)):
        if i == 0:
            print("Run: ", sys.argv[i]);
            continue;
        command += " " + sys.argv[i];
    p = Process( command );
    p.run();

if __name__ == "__main__":
    main();