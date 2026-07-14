import sys, os, inspect, socket, struct, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.append(ROOT);

from api.systemctl import Systemctl;
from api.resolv import Resolv;
from api.distro import Distro;
from api.process import Process;
from api.CONST import *;
# =========== INICIANDO SERVICOS E PROGRMAS ===============

def apontar_resolver(endereco):
    r = Resolv();
    r.clear();
    r.add("nameserver " + endereco);
    r.save();

def resolver_responde(host, port=53, nome="example.com", timeout=2):
    # Testa uma RESOLUCAO real no resolver local: monta uma query DNS tipo A e
    #    envia por TCP (o dnscrypt usa force_tcp). Retorna True so se vier uma
    #    resposta valida (mesmo ID, bit QR, rcode NoError e >=1 registro). Bem
    #    mais confiavel que o "active" do systemd, que nao prova que responde.
    try:
        tid = 0x1337;
        cabecalho = struct.pack(">HHHHHH", tid, 0x0100, 1, 0, 0, 0);  # RD=1, 1 pergunta
        pergunta = b"";
        for parte in nome.split("."):
            pergunta += bytes([len(parte)]) + parte.encode();
        pergunta += b"\x00" + struct.pack(">HH", 1, 1);               # QTYPE=A, QCLASS=IN
        msg = cabecalho + pergunta;
        pacote = struct.pack(">H", len(msg)) + msg;                   # DNS/TCP: prefixo de tamanho

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        s.settimeout(timeout);
        s.connect((host, int(port)));
        s.sendall(pacote);
        tam = s.recv(2);
        if len(tam) < 2:
            s.close();
            return False;
        (n,) = struct.unpack(">H", tam);
        dados = b"";
        while len(dados) < n:
            pedaco = s.recv(n - len(dados));
            if not pedaco:
                break;
            dados += pedaco;
        s.close();
        if len(dados) < 12:
            return False;
        rid, flags, qd, an, ns, ar = struct.unpack(">HHHHHH", dados[:12]);
        return rid == tid and (flags >> 15) & 1 == 1 and (flags & 0x000F) == 0 and an >= 1;
    except Exception:
        return False;

def esperar_resolver(host, port, tentativas=8, intervalo=1):
    # O dnscrypt leva alguns segundos pra subir (baixa a lista de resolvers),
    #    entao tentamos por ~8s antes de desistir.
    for _ in range(tentativas):
        if resolver_responde(host, port):
            return True;
        time.sleep(intervalo);
    return False;

def main():
    ctl = Systemctl( DNS_SERVICE );
    ctl.start();

    # Em Qubes o /etc/resolv.conf e gerenciado pela NetVM (10.139.1.1/2) e nunca
    #    o tocamos (safe-mode); logo nem precisamos testar o resolver local.
    if Distro().is_qubes():
        print("Qubes detectado: preservando o /etc/resolv.conf da NetVM.");
        return;

    # (B) Fail-closed de verdade: so repontamos o resolv.conf para o dnscrypt
    #     local se ele REALMENTE responde. Se nao, preservamos o resolver que ja
    #     funcionava — a pessoa nunca fica sem DNS por causa de um dnscrypt quebrado.
    if not esperar_resolver( DNS_LOCAL_RESOLVER, DNS_LISTEN_PORT ):
        print("dnscrypt nao respondeu em " + DNS_LOCAL_RESOLVER + ":" + str(DNS_LISTEN_PORT) + " — resolv.conf preservado.");
        print("(D) Para voltar ao DNS remoto/plaintext: kfm -p dns -c stop");
        return;

    print("Está rodando o serviço DNS Encrypt.");
    apontar_resolver( DNS_LOCAL_RESOLVER );

if __name__ == "__main__":
    main();
