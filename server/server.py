#!/usr/bin/env python

#-----------------------------------------------------------------------
# server.py
#-----------------------------------------------------------------------

from sys import exit, argv
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import time

BACKLOG = 5
chatLog = [] # This will be an array of tuples in the form (time, address, msg) 
connectionThreads = [] # Keep track of all connections so we can blast messages
#-----------------------------------------------------------------------

class ServerThread(Thread):
    def __init__(self, sock, address):
        Thread.__init__(self)
        self._sock = sock
        self._address = address

    # Opens a input stream that listens for new messages from client
    def run(self):
        print 'Spawned thread'
        inFlo = self._sock.makefile(mode='r')
        while True:
            line = inFlo.readline()
            if not line:
                break

            print line

            newMsg = (time(), self._address, line)
            chatLog.append(newMsg) # Keep track of all the chat messages ever received

            blastMessage(newMsg) # Send out new message to all connected clients

        inFlo.close()
        self._sock.close()
        print 'Closed socket'
        print 'Exiting thread'

        connectionThreads.remove(self) # Remove self from the list of threads

    def sendMsg(self, message):
        outFlo = self._sock.makefile(mode='w')
        outFlo.write(message)
        outFlo.close()

#-----------------------------------------------------------------------
def blastMessage(newMsg):
    for client in connectionThreads:
        (t, addr, msg) = newMsg
        (addr, port) = addr
        msg = str(t) + " " +  addr + " " + msg
        client.sendMsg(msg)

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
            serverThread = ServerThread(sock, address);
            serverThread.start();
            serverThread.sendMsg("Welcome to the LAN party!\n")
            connectionThreads.append(serverThread) # Add thread to list

    except Exception, e:
        print e

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)