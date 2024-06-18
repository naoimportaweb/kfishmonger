import sys, os, json, shutil, inspect;

ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
sys.path.append(ROOT);

from api.process import Process;
from api.apt import Apt;
from api.pip import Pip;

def main():
    files = os.listdir( ROOT );
    for file in files:
        directory_path =  ROOT + "/" + file ;
        config_pat = directory_path + "/config.json";
        if os.path.isdir(directory_path) and os.path.exists( config_pat ):
            config = json.loads( open( config_pat, "r"  ).read() );
            if config["default"]:
                print("Instalando: ", file);
                path_install = directory_path + "/install.py";
                process = Process( "python3 " + path_install );
                print(process.run().strip());
    print("Fim");

if __name__ == "__main__":
    apt = Apt();
    pip = Pip();
    apt.install("python3-pip");
    apt.install("python3-netifaces");
    main();