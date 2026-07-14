import sys, os, json, shutil, inspect;

ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
sys.path.append(ROOT);

from api.process import Process;
from api.empacotador import Empacotador;
from api.distro import Distro;
from api.pip import Pip;

def main():
    qubes = Distro().is_qubes();
    files = os.listdir( ROOT );
    for file in files:
        directory_path =  ROOT + "/" + file ;
        config_pat = directory_path + "/config.json";
        if os.path.isdir(directory_path) and os.path.exists( config_pat ):
            config = json.loads( open( config_pat, "r"  ).read() );
            roda = config["default"];
            # Em Qubes, modulos marcados com "qubes": false nao rodam (ex.: conky,
            #    que pinta na root window do X que o AppVM nem exibe).
            if qubes and config.get("qubes", True) == False:
                print("Pulando (incompativel com Qubes): ", file);
                roda = False;
            if roda:
                print("Instalando: ", file);
                path_install = directory_path + "/install.py";
                process = Process( "python3 " + path_install );
                print(process.run().strip());
    print("Fim");

if __name__ == "__main__":
    empacotador = Empacotador.detectar();
    pip = Pip();
    empacotador.install("python3-pip");
    empacotador.install("python3-netifaces");
    main();