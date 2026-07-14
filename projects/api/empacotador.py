import os, shutil;

from subprocess import STDOUT, check_call;
from .process import Process;


# Lê ID e ID_LIKE do /etc/os-release. É a fonte AUTORITATIVA de "quem governa o
#    sistema" — bem melhor que a mera presença do binário: um Debian pode ter o
#    dnf/rpm instalados como utilitário sem ser um sistema RPM.
def _ids():
    dados = {};
    try:
        with open("/etc/os-release") as f:
            for linha in f:
                linha = linha.strip();
                if linha == "" or linha[:1] == "#" or "=" not in linha:
                    continue;
                chave, valor = linha.split("=", 1);
                dados[chave] = valor.strip().strip('"');
    except FileNotFoundError:
        pass;
    return (dados.get("ID", "") + " " + dados.get("ID_LIKE", "")).lower();


# Classe base: define o CONTRATO que todo empacotador cumpre e a lógica
#    compartilhada (log, verbose, tradução de nomes e a fábrica detectar()).
class Empacotador():

    # Mapa nome-genérico -> nome-nesta-distro. Cada filho sobrescreve com os
    #    casos em que o nome do pacote diverge. Nome não mapeado é usado como está.
    NOMES = {};

    def __init__(self, log=None, verbose=False):
        self.log = log;
        self.verbose = verbose;

    def traduzir(self, package):
        return self.NOMES.get(package, package);

    def _log(self, msg):
        if self.log != None:
            self.log.info(msg);

    def _verbose(self, package):
        if self.verbose:
            print("\t:-) Pacote instalado: ", package);

    # Cada filho responde se ele governa este sistema. Prioridade: o ID do
    #    os-release (autoritativo); se não houver, cai no fallback por ferramenta.
    @classmethod
    def disponivel(cls):
        return False;

    # Em tempo de execução devolve a instância correta (Apt, Dnf, ...):
    #    empacotador = Empacotador.detectar();
    #    Varre as subclasses e usa a primeira cujo gerenciador existe. Adicionar
    #    um novo empacotador = criar a classe filha; esta fábrica nem muda.
    @staticmethod
    def detectar(log=None, verbose=False):
        for classe in Empacotador.__subclasses__():
            if classe.disponivel():
                return classe(log=log, verbose=verbose);
        raise RuntimeError("Nenhum empacotador suportado encontrado (apt/dnf/...).");

    # ---- Contrato: os filhos DEVEM implementar ----
    def update(self):
        raise NotImplementedError();

    def install(self, package):
        raise NotImplementedError();

    def exists(self, package):
        raise NotImplementedError();

    def instaled(self, package):
        raise NotImplementedError();

    def purge(self, package):
        raise NotImplementedError();

    def addrepo(self, repo):
        raise NotImplementedError();


# Debian / Ubuntu / Kali  (e AppVM Qubes com template Debian)
class Apt(Empacotador):

    NOMES = {};  # apt usa os nomes genéricos do projeto

    @classmethod
    def disponivel(cls):
        ids = _ids();
        if ids != "":
            return ("debian" in ids) or ("ubuntu" in ids) or ("kali" in ids);
        # Fallback (sem os-release): detecta pela ferramenta que governa.
        return shutil.which("apt-get") != None or os.path.isdir("/etc/apt");

    def update(self):
        check_call(['apt', 'update', '-y'], stdout=open(os.devnull, 'wb'), stderr=STDOUT);
        self._log("apt update executado.");

    def install(self, package):
        package = self.traduzir(package);
        os.system("apt install -y " + package);
        self._log("Instalando pacote " + package + " com APT.");
        self._verbose(package);

    def exists(self, package):
        package = self.traduzir(package);
        p = Process("apt-cache show " + package);
        return p.run().find("E: No packages found") < 0;

    def instaled(self, package):
        package = self.traduzir(package);
        p = Process("dpkg-query -W " + package);
        return p.run().find("no packages found matching") < 0;

    def purge(self, package):
        package = self.traduzir(package);
        check_call(['apt', 'purge', package, '-y'], stdout=open(os.devnull, 'wb'), stderr=STDOUT);

    def addrepo(self, repo):
        p = Process("echo \"deb https://deb.debian.org/debian/ " + repo + " main\" | sudo tee /etc/apt/sources.list.d/" + repo + ".list");
        p.run();
        Process("apt update -y").run();


# Fedora / RHEL / CentOS  (e AppVM Qubes com template Fedora)
class Dnf(Empacotador):

    NOMES = {
        "conky-all": "conky",  # no Debian é conky-all; no Fedora é conky
    };

    @classmethod
    def disponivel(cls):
        ids = _ids();
        if ids != "":
            return ("fedora" in ids) or ("rhel" in ids) or ("centos" in ids);
        # Fallback (sem os-release): detecta pela ferramenta que governa.
        return shutil.which("dnf") != None;

    def update(self):
        # check-update sai com código 100 quando há atualizações; os.system
        #    evita a exceção que o check_call levantaria.
        os.system("dnf check-update");
        self._log("dnf check-update executado.");

    def install(self, package):
        package = self.traduzir(package);
        os.system("dnf install -y " + package);
        self._log("Instalando pacote " + package + " com DNF.");
        self._verbose(package);

    def exists(self, package):
        package = self.traduzir(package);
        saida = Process("dnf list " + package).run();
        return saida.strip() != "" and saida.find("Error") < 0;

    def instaled(self, package):
        package = self.traduzir(package);
        saida = Process("rpm -q " + package).run();
        return saida.find("is not installed") < 0;

    def purge(self, package):
        package = self.traduzir(package);
        os.system("dnf remove -y " + package);

    def addrepo(self, repo):
        os.system("dnf config-manager --add-repo " + repo);


def main():
    e = Empacotador.detectar();
    print("Empacotador:", type(e).__name__);

if __name__ == "__main__":
    main();
