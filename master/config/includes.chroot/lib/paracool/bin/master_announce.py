import socket
import os.path
import time


def debug_message(message):
    if os.path.exists("/lib/paracool/DEBUG"):
        print "debug - {} {}".format(time.strftime("%H:%M:%S", time.gmtime()), message)


my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
while True:
    if not os.path.exists("/lib/paracool/CLUSTER_CONFIG"):
        break
    try:
        my_socket.sendto("MASTER ANNOUNCE", ('<broadcast>' ,8881))
        debug_message("Sending Master Announce")
    except:
        debug_message("Network not ready. Waiting...")
    time.sleep(3)


my_socket.close()
