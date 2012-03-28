#!/usr/bin/env python

#-----------------------------------------------------------------------
# client.py
#-----------------------------------------------------------------------

from sys import exit, argv, stdin
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
import sys
import ConfigParser
import json

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

		self._inFlo = self._sock.makefile('r')

		while True:
			line = self._inFlo.readline()
			if not line:
				break
			self._receivedMessages.append(line)
			
			print line
		
		self.quitThread()
	
	def quitThread(self):
		self._inFlo.close()
		self._sock.close()
		print 'Quitting listener thread...'
		self._Thread__stop()
    
class ClientConnect(object):
	def __init__(self, serverip):
		self._serverip = serverip
		self.connectToServer()

	def connectToServer(self):
		try:
			host = ".".join([str(i) for i in self._serverip])

			sock = socket(AF_INET, SOCK_STREAM)
			sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
			sock.connect((host, port))
			print 'Client IP addr and port:', sock.getsockname()
			print 'Server IP addr and port:', sock.getpeername()

			self._clientReceiveThread = ClientReceiveThread(sock)
			self._clientReceiveThread.start()

			self._receivedMessages = self._clientReceiveThread._receivedMessages
			self._sock = sock
		except Exception, e:
			print e

	def sendToServer(self, msg):
		outFlo = self._sock.makefile(mode='w')
		outFlo.write(msg + "\n")
		outFlo.flush()
		outFlo.close()
	
	def sendDict(self, d):
		dictstr = json.dumps(d)
		self.sendToServer(dictstr)
	
	def quitThread(self):
		self._sock.close()
		self._clientReceiveThread.quitThread()
		print "Quit server listener"

#-----------------------------------------------------------------------

if __name__ == '__main__':
	import time
	obj = ClientConnect([127,0,0,1])
	i = 0
	while True:
		i += 1
		time.sleep(1)
		obj.sendToServer(str(i) + "\n")
		print obj._receivedMessages
