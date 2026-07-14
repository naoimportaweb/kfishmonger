import sys, os, shutil, inspect, subprocess;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.systemctl import Systemctl;
from api.empacotador import Empacotador;
from api.process import Process;
from api.log import Log;
from api.config_project import ConfigProject;
from api.CONST import *;

# =========== INSTALAÇÃO DE DEPENDENCIAS ==================
log = Log("dns");

if os.path.exists("/etc/dnscrypt-proxy/linux-x86_64/dnscrypt-proxy"):
    print("Já está instalado (será reinstalado/atualizado).");

# minisign e usado para verificar a assinatura do binario baixado.
empacotador = Empacotador.detectar(log=log);
empacotador.install("minisign");

config_project = ConfigProject("dns", log=log);
config_project.copy();

# =========== PARAMETROS DA RELEASE ==================
# OBS: arch fixa em x86_64 (o path /etc/dnscrypt-proxy/linux-x86_64 tambem e
#    usado no execstart.py/status.py). Qubes e os alvos multi-distro sao x86_64.
ARCH = "x86_64";
BASE = "dnscrypt-proxy-linux_" + ARCH + "-" + DNS_VERSION + ".tar.gz";
URL  = "https://github.com/DNSCrypt/dnscrypt-proxy/releases/download/" + DNS_VERSION + "/" + BASE;
TAR  = "/tmp/" + BASE;
SIG  = TAR + ".minisig";

# =========== LIMPEZA DE RESTOS ==================
for caminho in ["/tmp/linux-" + ARCH, TAR, SIG]:
    if os.path.isdir(caminho):
        shutil.rmtree(caminho, ignore_errors=True);
    elif os.path.exists(caminho):
        os.unlink(caminho);

def baixar(url, destino):
    r = subprocess.run(["wget", "-q", url, "-O", destino]);
    return r.returncode == 0 and os.path.exists(destino) and os.path.getsize(destino) > 0;

def abortar(msg):
    log.error(msg);
    print("ERRO: " + msg + " Nada foi instalado.");
    for f in [TAR, SIG]:
        if os.path.exists(f):
            os.unlink(f);
    sys.exit(1);

# =========== DOWNLOAD (binario + assinatura) ==================
print("[+] Baixando " + URL);
if not baixar(URL, TAR):
    abortar("Falha no download do dnscrypt-proxy " + DNS_VERSION + ".");
if not baixar(URL + ".minisig", SIG):
    abortar("Falha no download da assinatura (.minisig).");
log.download(TAR, URL);

# =========== VERIFICACAO DA ASSINATURA (minisign) ==================
# Sem isso instalariamos um binario nao confiavel como resolver DNS do sistema.
#    A chave publica e a oficial do projeto dnscrypt (fixa em CONST).
print("[+] Verificando assinatura minisign...");
verificacao = subprocess.run(["minisign", "-Vm", TAR, "-P", DNSCRYPT_MINISIGN_KEY]);
if verificacao.returncode != 0:
    abortar("Assinatura minisign INVALIDA (possivel adulteracao/corrupcao).");
log.info("Assinatura minisign verificada com sucesso para " + BASE + ".");

# =========== EXTRACAO E INSTALACAO ==================
os.makedirs("/tmp/linux-" + ARCH, exist_ok=True);
Process("tar --strip-components 1 -C /tmp/linux-" + ARCH + "/ -xzf " + TAR).run();
os.makedirs("/etc/dnscrypt-proxy", exist_ok=True);
Process("cp -r /tmp/linux-" + ARCH + "/ /etc/dnscrypt-proxy/").run();

# Diretorios exigidos pelo toml (query_log, nx_log e cache dos resolvers);
#    sem eles o dnscrypt-proxy nao sobe.
os.makedirs("/var/log/dnscrypt-proxy", exist_ok=True);
os.makedirs("/var/cache/dnscrypt-proxy", exist_ok=True);

shutil.copy( CURRENTDIR + "/resources/" + DNS_SERVICE, "/etc/systemd/system/");

if not os.path.exists("/var/kfm/dns/blocked-names.txt"):
    shutil.copy( CURRENTDIR + "/resources/blocked-names.txt", "/var/kfm/dns/");

ctl = Systemctl( DNS_SERVICE );
ctl.reload();
ctl.enable();
ctl.start();
if ctl.status():
    print("Está rodando o serviço DNS Crypt");
else:
    print("NÃO está rodando o serviço DNS Crypt");

ctl = Systemctl("dnscrypt-proxy");
if ctl.exists():
    ctl.disable();
    ctl.stop();
