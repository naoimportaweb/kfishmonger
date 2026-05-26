#https://github.com/ysc3839/FakeSSHServer/blob/master/FakeSSHServer.py
import os , sys, threading, traceback, paramiko, socket, socketserver, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR));
sys.path.append(ROOT);
sys.path.append(ROOT + "/panicroom/");

from api.log import Log;
from api.rsahelp import RSAHelp;
from binascii import hexlify;
from api.panicroomclient import PanicRoomClient;

log = Log("fake_ssh");
rsa = RSAHelp();
panicroom = PanicRoomClient();

PORT = 22
RETURN_MESSAGE = None
PATH_RSA_PRIVATE="/var/kfm/fake/rsa_private.txt"

if not os.path.exists(PATH_RSA_PRIVATE):
    with open(PATH_RSA_PRIVATE, "w") as f:
        f.write( rsa.make()[0] );
host_key = paramiko.RSAKey(filename=PATH_RSA_PRIVATE);

class Server (paramiko.ServerInterface):
    def __init__(self, client_address):
        self.event = threading.Event()
        self.client_address = client_address

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        print('IP: %s, User: %s, Password: %s' % (self.client_address[0], username, password));
        log.info('IP: %s, User: %s, Password: %s' % (self.client_address[0], username, password))
        panicroom.send_alert("ALERT", 'Tentativa indevida de acesso ao SSH Fake. User: %s, Password: %s' % (username, password));
        return paramiko.AUTH_FAILED; # sempre dropar a negociação USUARIO/SENHA.

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
                                  pixelheight, modes):
        return True

class SSHHandler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            t = paramiko.Transport(self.connection)
            t.add_server_key(host_key)
            server = Server(self.client_address)
            try:
                t.start_server(server=server)
            except paramiko.SSHException:
                print('Falha de negociação SSH.')
                return
            chan = t.accept(20)
            if chan is None:
                t.close()
                return

            server.event.wait(10)
            if not server.event.is_set():
                t.close()
                return

            if RETURN_MESSAGE != None:
                chan.send(RETURN_MESSAGE)
            chan.close()

        except Exception as e:
            print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
            traceback.print_exc()
        finally:
            try:
                t.close()
            except:
                pass

sshserver = socketserver.ThreadingTCPServer(("0.0.0.0", PORT), SSHHandler)
sshserver.serve_forever()