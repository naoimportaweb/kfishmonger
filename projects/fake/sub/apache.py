import socket, psutil;
import sys, os, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR));
sys.path.append(ROOT);
sys.path.append(ROOT + "/panicroom/");

from api.log import Log;
from api.panicroomclient import PanicRoomClient;

log = Log("fake_http");
panicroom = PanicRoomClient();

def porta_aberta():
    portas = [80];
    for i in range(1000):
        portas.append( 8080 + i );
    abertos = psutil.net_connections();
    portas_abertas = [];
    for aberto in abertos:
        if len(aberto[4]) > 0:
            portas_abertas.append(aberto[4][1]);
    for porta in portas:
        if not porta in portas_abertas:
            return porta;

def main():
    HOST     = "127.0.0.1";
    PORT     = porta_aberta();
    RESPONSE = 'HTTP/1.1 200 OK\r\nServer: Apache/2.4.59 (Debian)\r\nAccept-Ranges: bytes\r\nContent-Length: 26\r\nVary: Accept-Encoding\r\nContent-Type: text/html\r\n\r\n\n<html><body></body></html>'
    log.info("Serviço aberto na porta: " + str( PORT ));
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT));
        s.listen();
        while True:    
            conn, addr = s.accept();
            with conn:
                data = conn.recv(4096).decode().replace("\r", "");
                log.info("Conexão recebida: " + addr[0] + ":" + str(addr[1]) + " - " + data.split("\n")[0] );
                panicroom.send_alert("ALERT", "Uma requisição feita ao serviço HTTP Fake.");
                conn.sendall( RESPONSE.encode() );

if __name__ == "__main__":
    main();