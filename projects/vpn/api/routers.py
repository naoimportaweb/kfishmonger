#!/usr/bin/python3

import os, re, socket, subprocess, struct;

class Routers():
    def __init__(self):
        self.path_ovpn = "/var/kfm/vpn/openvpn.ovpn";

    def get_default_gateway_linux(self):
        with open("/proc/net/route") as fh:
            for line in fh:
                fields = line.strip().split()
                if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                    continue
                return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

    def translate_domain(self, domain):
        try:
            lista = list( map( lambda x: x[4][0], socket.getaddrinfo( domain ,22,type=socket.SOCK_STREAM)));
            ips = [];
            for buffer in lista:
                ip = self.cut_ip(buffer);
                if not ip == None and not ip in ips:
                    ips.append(ip);
            return ips;
        except:
            print("Nao foi traduzido:", domain);
        return [];

    def cut_ip(self, linha):
        retorno = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", linha)
        if len(retorno) > 0:
            return linha;

    def find_ips(self):
        ips = [];
        with open(self.path_ovpn, "r") as f:
            linhas = f.readlines();
            for linha in linhas:
                linha = linha.strip();
                if linha[:len("remote")] == "remote":
                    partes = linha.split(" ");
                    if len(partes) < 2:
                        continue;
                    ip = self.cut_ip(partes[1]);
                    if ip == None: # pode ser um dominio, exemplo: server1vpn.proton.net
                        buffer_ips_traduzidos = self.translate_domain(partes[1]);
                        for buffer_ip_traduzido in buffer_ips_traduzidos:
                            ips.append(buffer_ip_traduzido);
                    if not ip == None and not ip in ips:
                        ips.append(ip);
        return ips;

    def kill(self, gateway_ip):
        ips = self.find_ips();
        print("KILL switch");
        subprocess.call(["ip", "route", "del", "default"]);
        for ip in ips:
            subprocess.call(["ip", "route", "add", ip ,"via", gateway_ip]);

    def deskill(self, gateway_ip):
        ips = self.find_ips();
        for ip in ips:
            subprocess.call(["ip", "route", "del", ip ]);
        subprocess.call(["ip", "route", "add", "default", "via", gateway_ip]);

#def main():
#    gateway_ip = get_default_gateway_linux();
#    if gateway_ip == None:
#        gateway_ip = input("Digite o IP do Router Gateway da rede: ");
#
#    if cut_ip(gateway_ip) == None:
#        print("Isso nao e um ip valido. bye");
#        return;
#
#    while True:
#        decisao = input('\n\nDigite (d) para desligar o KillSwitch ou (l) para ligar o KillSwitch. (s) para sair: ')
#        if decisao == "l":
#            kill(gateway_ip);
#            print("\nRESULTADO:");
#            subprocess.call(["ip", "route"]);
#        elif decisao == "d":
#            deskill(gateway_ip);
#            print("\nRESULTADO:");
#            subprocess.call(["ip", "route"]);
#        else:
#            print("bye");
#            return;
if __name__ == "__main__":
    #main();
    r = Routers();
    print( r.get_default_gateway_linux() );