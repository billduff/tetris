#!/usr/bin/env python

#-----------------------------------------------------------------------
# client.py
#-----------------------------------------------------------------------

from sys import exit, argv, stdin
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
#-----------------------------------------------------------------------

class ClientThread(Thread):
    def __init__(self, sock):
        Thread.__init__(self)
        self._sock = sock

    def run(self):
        print 'Listening for new messages from server'
        
        inFlo = self._sock.makefile('r')

        while True:
            line = inFlo.readline()
            if not line:
                break

	    print line
            
            print line
            
        inFlo.close()
        print 'Exiting thread'
            
def main(argv):

    if len(argv) != 3:
        print 'Usage: python %s host port' % argv[0]
        exit(1)

    try:
        host = argv[1]
        port = int(argv[2])

        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((host, port))
        print 'Client IP addr and port:', sock.getsockname()
        print 'Server IP addr and port:', sock.getpeername()

        outFlo = sock.makefile(mode='w') 

        clientThread = ClientThread(sock)
        clientThread.start()

        while True:
            line = stdin.readline()
            if not line:
                break
            outFlo.write(line)
            outFlo.flush()

        outFlo.close()
        sock.close()

    except Exception, e:
        print e

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
