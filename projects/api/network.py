import re, os, sys
import socket, json
import requests
from requests import adapters
from urllib3.poolmanager import PoolManager

from process import Process;

class Network():
    def __init__(self):
        self.devices = [];
        self.list_devices();

    def default(self):
        p = Process("ip route");
        linhas = p.run().split("\n");
        for linha in linhas:
            if linha.split(" ")[0] == "default":
                return linha.split(" ")[4];
        return None;

    def tunnels(self):
        buffer = [];
        for device in self.devices:
            if device.type == "tun" and self.test( device.name ):
                buffer.append( device.name );
        return buffer;

    def test(self, interface):
        try:
            self.location(interface=interface);
            return True;
        except:
            return False;
    
    def location(self, interface=None, proxy=None):
        if interface == None:
            interface = self.default();
        if interface == None:
            return None;
        session = requests.Session();
        if proxy != None:
            session.proxies = {'http':  proxy, 'https': proxy};

        for prefix in ('http://', 'https://'):
            session.mount(prefix, InterfaceAdapter(iface=interface.encode()))
        return json.loads(session.get('https://wtfismyip.com/json').text);

    def list_devices(self):
        p = Process("nmcli connection show")
        self.devices = [];
        linhas = p.run().split("\n");
        index_name   = 0;
        index_uuid   = linhas[0].find("UUID");
        index_type   = linhas[0].find("TYPE");
        index_device = linhas[0].find("DEVICE");

        for i in range(len(linhas)):
            if i == 0:
                continue;
            name = linhas[i][ index_name : index_uuid ];
            uuid = linhas[i][ index_uuid : index_type ];
            type = linhas[i][ index_type : index_device ];
            devi = linhas[i][ index_device :  ];
            if name.strip() == "":
                continue;

            buffer = Device( name.strip(), uuid.strip(), type.strip(), devi.strip() );
            self.devices.append( buffer );

class Device():
    def __init__(self, name, uuid, type, device):
        self.name = name;
        self.uuid = uuid;
        self.type = type;
        self.device = device;
    def toString(self):
        return self.name, self.uuid, self.type, self.device;

class InterfaceAdapter(adapters.HTTPAdapter):

    def __init__(self, **kwargs):
        self.iface = kwargs.pop('iface', None)
        super(InterfaceAdapter, self).__init__(**kwargs)

    def _socket_options(self):
        if self.iface is None:
            return []
        else:
            return [(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, self.iface)]

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            socket_options=self._socket_options()
        )
if __name__ == "__main__":
    n = Network();
    print( n.tunnels() );
    #print( n.location() ); # ISSO AQUI VAI MOSTRAR O SEU IP NAO IMPORTA O QUE ESTEJA USANDO
    #print( n.location(interface="tun0") );
    #print( n.location(interface="tun0", proxy='socks5://127.0.0.1:9050') );

