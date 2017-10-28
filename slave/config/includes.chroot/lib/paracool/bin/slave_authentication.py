# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


"""
An example client. Run simpleserv.py first before running this.
"""

from twisted.internet import reactor, protocol
import socket
import time
import Crypto.PublicKey.RSA as rsa
import os
authenticated = False

def debug_message(message):
    if os.path.exists("/lib/paracool/DEBUG"):
        print "debug - {} {}".format(time.strftime("%H:%M:%S", time.gmtime()),message)
# a client protocol

class AuthClient(protocol.Protocol):

    """Once connected, send a message, then print the result."""
    def __init__(self):
        self.state = "UNAUTH"
    def connectionMade(self):
        debug_message("Connected to Auth server.")

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        if self.state == "UNAUTH":
            self.rand_str = data[:-1]
            encrypted_str = pubkey.encrypt(self.rand_str,16)[0].encode('base64')
            self.transport.write(encrypted_str+"\n")
            self.state = "PENDING"
            return
        else:
            if "OK" in data:
                print "Master authentication OK!"
                global authenticated
                uid = int(data[:-4])
                with open('/lib/paracool/UID','w') as f:
                    f.write(str(uid))
                authenticated=True

            else:
                print "Master authentication FAILED!"
            self.transport.loseConnection()



    def connectionLost(self, reason):
        return


class AuthFactory(protocol.ClientFactory):
    protocol = AuthClient

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        reactor.stop()

with open("/lib/paracool/keys/id_rsa.pub") as f:
    pubkey = rsa.importKey(f.read())



my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
my_socket.bind(('',8881))

print 'Start listening for Master announces ...'


while True :
    message , address = my_socket.recvfrom(8192)
    if str(message) == "MASTER ANNOUNCE":
        debug_message("Got master on {}".format(address[0]))
        master_host = address[0]
        break
my_socket.close()


HOST, PORT = master_host, 9999

f = AuthFactory()
reactor.connectTCP(HOST, PORT, f)
reactor.run()
if authenticated:
    with open("/lib/paracool/MASTER_IP","w") as f:
        f.writelines(master_host+"\n")