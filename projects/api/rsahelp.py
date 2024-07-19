import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast

class RSAHelp():
    def make(self):
        keyPair = RSA.generate(1024);
        pubKey = keyPair.publickey()
        pubKeyPEM = pubKey.exportKey()
        privKeyPEM = keyPair.exportKey()
        return (privKeyPEM.decode('ascii'), pubKeyPEM.decode('ascii'));

