import sys, os, shutil, inspect, time, traceback, random, re, socket;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR));
sys.path.append(ROOT);

from api.config import Config;

class Openvpn():
    def __init__(self):
        self.path = "/var/kfm/vpn/";
        self.ovpn_lines = None;
        self.migrate();
    #customizar da versao antiga para nova vers'ao
    def migrate(self):
        files = os.listdir( self.path );
        exists = False;
        for file in files:
            if os.path.isdir( self.path + "/" + file):
                print(self.path + "/" + file);
                exists = True;
                break;
        if not exists and os.path.exists(self.path + "/openvpn.ovpn"):
            os.mkdir(self.path + "/default");
            if os.path.exists(self.path + "/openvpn.ovpn"):
                shutil.copy(self.path + "/openvpn.ovpn", self.path + "/default/openvpn.ovpn");
            if os.path.exists(self.path + "/ca.crt"):
                shutil.copy(self.path + "/ca.crt", self.path + "/default/ca.crt");
            if os.path.exists(self.path + "/client.crt"):
                shutil.copy(self.path + "/client.crt", self.path + "/default/client.crt");
            if os.path.exists(self.path + "/client.key"):
                shutil.copy(self.path + "/client.key", self.path + "/default/client.key");
            if os.path.exists(self.path + "/pass.txt"):
                shutil.copy(self.path + "/pass.txt", self.path + "/default/pass.txt");
    
    def __cut_ip__(self, linha):
        retorno = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", linha)
        if len(retorno) > 0:
            return linha;

    def __translate_domain__(self, domain):
        try:
            lista = list( map( lambda x: x[4][0], socket.getaddrinfo( domain ,22,type=socket.SOCK_STREAM)));
            ips = [];
            for buffer in lista:
                ip = self.__cut_ip__(buffer);
                if not ip == None and not ip in ips:
                    ips.append(ip);
            return ips;
        except:
            print("Nao foi traduzido:", domain);
        return [];

    def load(self, path):
        self.ovpn_lines = open(path + "/openvpn.ovpn", "r").readlines();
        for i in range(len(self.ovpn_lines)):
            self.ovpn_lines[i] = self.ovpn_lines[i].strip();
        # procurar por: remote kkkkkkkk.com.br NUMBER e fazer a traducao por IP.
        for i in range(len(self.ovpn_lines)):
            if self.ovpn_lines[i][:len("remote ")] == "remote ":
                partes = self.ovpn_lines[i].split(" ");
                if len(partes) < 2:
                    continue;
                ip = self.__cut_ip__(partes[1]);
                if ip == None: # pode ser um dominio, exemplo: server1vpn.proton.net
                    buffer_ips_traduzidos = self.__translate_domain__(partes[1]);
                    if len(buffer_ips_traduzidos) > 0:
                        ip = buffer_ips_traduzidos[0];
                if ip != None:
                    self.ovpn_lines[i] = "remote " + ip + " " + partes[2];
        # agora colocar caminho fixo para os certificados
        ca_path = None;
        key_path = None;
        cert_path = None;

        for i in range(len(self.ovpn_lines)):
            if self.ovpn_lines[i][:len("ca ")] == "ca ":
                partes = self.ovpn_lines[i].split(" ");
                if partes[1].find("/") == 0:
                    ca_path = partes[1];
                else:
                    self.ovpn_lines[i] = "ca /var/kfm/vpn/ca.crt";
                    ca_path = path + "/" + partes[1];
        for i in range(len(self.ovpn_lines)):
            if self.ovpn_lines[i][:len("cert ")] == "cert ":
                partes = self.ovpn_lines[i].split(" ");
                if partes[1].find("/") == 0:
                    cert_path =  partes[1];
                else:
                    self.ovpn_lines[i] = "cert /var/kfm/vpn/client.crt";
                    cert_path = path + "/" + partes[1];
        for i in range(len(self.ovpn_lines)):
            if self.ovpn_lines[i][:len("key ")] == "key ":
                partes = self.ovpn_lines[i].split(" ");
                if partes[1].find("/") == 0:
                    key_path = partes[1];
                else:
                    self.ovpn_lines[i] = "key /var/kfm/vpn/client.key";
                    key_path = path + "/" + partes[1];
        print(ca_path);
        if ca_path != None:
            if ca_path != "/var/kfm/vpn/ca.crt":
                shutil.copy(ca_path, "/var/kfm/vpn/ca.crt");
            if key_path != "/var/kfm/vpn/client.key":
                shutil.copy(key_path, "/var/kfm/vpn/client.key");
            if cert_path != "/var/kfm/vpn/client.crt":
                shutil.copy(cert_path, "/var/kfm/vpn/client.crt");
        if os.path.exists(path + "/pass.txt"):
            shutil.copy(path + "/pass.txt", "/var/kfm/vpn/pass.txt");

    def save(self):    
        with open("/var/kfm/vpn/openvpn.ovpn","w" ) as f:
            for i in range(len(self.ovpn_lines)):
                f.write(self.ovpn_lines[i] + "\n");

    def loadrandom(self):
        files = os.listdir( self.path );
        candidatos = [];
        for file in files:
            if os.path.isdir( self.path + "/" + file) and os.path.exists(self.path + "/" + file + "/openvpn.ovpn") and os.path.exists(self.path + "/" + file + "/pass.txt"):
                candidatos.append(file);
        index = 0;
        if len(candidatos) > 0:
            index = random.randint(0, len(candidatos) - 1);
        return self.load(self.path + "/" + candidatos[index]);

def main():
    ovpn = Openvpn();
    ovpn.loadrandom();
    ovpn.save();

if __name__ == "__main__":
    main();