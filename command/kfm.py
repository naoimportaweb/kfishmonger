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

def restart( project ):
    p = Process( "python3 " + ROOT + "/projects/"+ project +"/restart.py", wait=False );
    print(p.run());    

def start( project ):
    p = Process( "python3 " + ROOT + "/projects/"+ project +"/start.py", wait=False );
    print(p.run());    

def main():
    parser = argparse.ArgumentParser(description="");
    parser.add_argument("-c","--command", required=True);
    parser.add_argument("-p","--project", nargs="?", const="", default="");
    args = parser.parse_args();
    if args.command == "install":
        if args.project == "":
            install_all();
        else:
            install_project( args.project );
    elif args.command == "restart":
        restart(args.project);
    elif args.command == "start":
        start(args.project);

if __name__ == "__main__":
    main();