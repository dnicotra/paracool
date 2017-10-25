from twisted.internet import reactor,protocol
import string
import random
import time
import os
import Crypto.PublicKey.RSA as rsa


def add_slave(slave_ip):
    if os.path.exists("/home/user/machine_file"):
        with open("/home/user/machine_file","r") as f:
            for line in f.readlines():
                if slave_ip in line:
                    return
    if os.path.exists("/etc/hosts.allow"):
        with open("/etc/hosts.allow","r") as f:
            for line in f.readlines():
                if slave_ip in line:
                    return

    with open('/etc/hosts.allow','a') as f:
        f.writelines("[ALL]:"+slave_ip + "\n")

    with open('/home/user/machine_file','a') as f:
        f.writelines(slave_ip + "\n")

def debug_message(message):
    if os.path.exists("/lib/paracool/DEBUG"):
        print "debug - {} {}".format(time.strftime("%H:%M:%S", time.gmtime()), message)


def generate_random_string(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


class MyProtocol(protocol.Protocol):
    def __init__(self):
        self.rand_str = generate_random_string(128)

    def connectionMade(self):
        debug_message("connection from " + str(self.transport.getPeer()))
        debug_message("Sending authetication string...")
        self.transport.write(self.rand_str + "\n")

    def dataReceived(self, data):
        try:
            decoded = data[:-1].decode('base64')
            decrypted = privkey.decrypt(decoded)
            if decrypted == self.rand_str:
                print("Got Slave @ " + self.transport.getPeer().host)
                #CONFIGURING
                add_slave(self.transport.getPeer().host)
                self.transport.write("OK\n")
            else:
                raise
        except:
            self.transport.abortConnection()
            debug_message("Auth FAILED @ " + self.transport.getPeer().host)
            return
    def connectionLost(self,reason):
        return

with open("/lib/paracool/keys/id_rsa","r") as f:
    privkey = rsa.importKey(f.read())
f = protocol.ServerFactory()
f.protocol = MyProtocol
reactor.listenTCP(9999, f)
reactor.run()