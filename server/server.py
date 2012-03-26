#!/usr/bin/env python

#-----------------------------------------------------------------------
# echoservermult.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import exit, argv
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

BACKLOG = 5

#-----------------------------------------------------------------------

class ServerThread(Thread):
    def __init__(self, sock):
        Thread.__init__(self)
        self._sock = sock
    def run(self):
        print 'Spawned thread'
        inFlo = self._sock.makefile(mode='r')
        outFlo = self._sock.makefile(mode='w')
        while True:
            line = inFlo.readline()
            if not line:
                break
            outFlo.write('Echo: ' + line)
            outFlo.flush()
        inFlo.close()
        outFlo.close()
        self._sock.close()
        print 'Closed socket'
        print 'Exiting thread'

#-----------------------------------------------------------------------

def main(argv):

    if len(argv) != 2:
        print 'Usage: python %s port' % argv[0]
        exit(1)

    try:
        port = int(argv[1])

        serverSock = socket(AF_INET, SOCK_STREAM)
        print 'Opened server socket'
        serverSock.bind(('', port))
        print 'Bound server socket to port'
        serverSock.listen(BACKLOG)
        print 'Listening'

        while True:
            sock, address = serverSock.accept()
            print 'Accepted connection, opened socket'
            serverThread = ServerThread(sock);
            serverThread.start();

    except Exception, e:
        print e

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
