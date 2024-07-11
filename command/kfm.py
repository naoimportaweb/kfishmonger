#!/usr/bin/python3
import os, sys, argparse;
import json, shutil, inspect;

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))));
sys.path.append(ROOT + "/projects/");

from api.process import Process;

def install_all():
    p = Process( "python3 " + ROOT + "/projects/install.py" );
    print(p.run());

def install_project(project):
    p = Process( "python3 " + ROOT + "/projects/"+ project +"/install.py" );
    print(p.run());

def install_sub_project(project, sub):
    p = Process( "python3 " + ROOT + "/projects/"+ project +"/sub/"+ sub +"/install.py" );
    print(p.run());

def command(project, command):
    file = ROOT + "/projects/"+ project +"/"+ command +".py";
    if not os.path.exists( file ):
        print("O comando não existe: ", command);
        return;
    p = Process( "python3 " + file , wait=False );
    print(p.run());    

def main():
    parser = argparse.ArgumentParser(description="");
    parser.add_argument("-c","--command", required=True);
    parser.add_argument("-b","--background", nargs="?", const="", default="");
    parser.add_argument("-p","--project", nargs="?", const="", default="");
    parser.add_argument("-s","--sub", nargs="?", const="", default="");
    args = parser.parse_args();
    if args.command == "install":
        if args.project == "":
            install_all();
        else:
            if args.sub == "":
                install_project( args.project );
            else:
                install_sub_project( args.project, args.sub  );
    elif args.command == "update":
        p = Process("/bin/bash /opt/kfishmonger/command/update.sh");
        p.run();
    else:
        command(args.project, args.command);

if __name__ == "__main__":
    main();