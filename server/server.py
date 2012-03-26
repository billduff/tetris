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
        self._outFlo = self._sock.makefile(mode='w')
        self._outFlo.write("Welcome to the LAN party!")

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
        outFlo.close()
        self._sock.close()
        print 'Closed socket'
        print 'Exiting thread'

        # connectionThreads.remove(self)

    def sendMsg(self, message):
        (t, addr, msg) = message
        (addr, port) = addr
        msg = str(t) + " " +  addr + " " + msg
        print "SEND MSG: ", msg
        self._outFlo.write(msg)

#-----------------------------------------------------------------------
def blastMessage(newMsg):
    for client in connectionThreads:
        print client
        client.sendMsg(newMsg)

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

            outFlo = sock.makefile(mode="w")
            outFlo.write("Welcome to the LAN party!")
            outFlo.close()

            serverThread = ServerThread(sock, address);
            serverThread.start();
            connectionThreads.append(serverThread) # Add thread to list

    except Exception, e:
        print e

#-----------------------------------------------------------------------

#Functions to convert ip <-> words

f = open("wordlist.txt")
ipwords = f.read()
f.close()

ipwords = ipwords.split(",") 

def ipToWords(ip):
	ipstr = ""
	for i in ip:
		ipstr += ipwords[i] + " "
	ipstr = ipstr[:-1] #remove trailing space
	return ipstr

def wordsToIP(words):
    ip = []
    for word in words.split(' '):
        i = 0
        ipword = ipwords[ip]
        while ipword != word:
            i += 1
            ipword = ipwords[ip]
        ip.append(i)

if __name__ == '__main__':
    main(argv)
