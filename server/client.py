#!/usr/bin/env python

#-----------------------------------------------------------------------
# client.py
#-----------------------------------------------------------------------

from sys import exit, argv, stdin
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import ConfigParser

#-----------------------------------------------------------------------

config = ConfigParser.ConfigParser()
config.read("tetrisrc.conf")

port = int(config.get("configvalues","port"))

class ClientReceiveThread(Thread):
	def __init__(self, sock):
		Thread.__init__(self)
		self._sock = sock
		self._receivedMessages = []

	def run(self):
		print 'Listening for new messages from server'
		
		inFlo = self._sock.makefile('r')

		while True:
			line = inFlo.readline()
			if not line:
				break
			self._receivedMessages.append(line)
			
		inFlo.close()
		print 'Exiting thread'
						
def connectToServer(serverip):

	try:
		host = ".".join([str(i) for i in serverip])

		sock = socket(AF_INET, SOCK_STREAM)
		sock.connect((host, port))
		print 'Client IP addr and port:', sock.getsockname()
		print 'Server IP addr and port:', sock.getpeername()

		clientReceiveThread = ClientReceiveThread(sock)
		clientReceiveThread.start()

		return (clientReceiveThread, sock)

	except Exception, e:
		print e

def sendToServer(sock, msg):
	outFlo = sock.makefile(mode='w')
	outFlo.write(msg)
	outFlo.flush()
	outFlo.close()

#-----------------------------------------------------------------------

if __name__ == '__main__':
	import time
	(crecv, sock) = connectToServer([127,0,0,1])
	i = 0
	while True:
		i += 1
		time.sleep(1)
		sendToServer(sock,str(i) + "\n")
		print crecv._receivedMessages
