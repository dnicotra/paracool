import socket
import os.path
import time


def debug_message(message):
    if os.path.exists("/lib/paracool/DEBUG"):
        print "debug - {} {}".format(time.strftime("%H:%M:%S", time.gmtime()), message)


my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
n_err = 0
while True:
    try:
        my_socket.sendto("MASTER ANNOUNCE", ('<broadcast>' ,8881))
        debug_message("Sending Master Announce")
        n_err=0
    except:
        if n_err<20:
            debug_message("Network Error. Waiting...")
        else:
            debug_message("Network unavaiable for 60 seconds. Check settings then restart.")
            break
    time.sleep(3)


my_socket.close()
