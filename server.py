#!/usr/bin/env python

#-----------------------------------------------------------------------
# server.py
#-----------------------------------------------------------------------

from sys import exit, argv
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import time
import iputils
import json
import ConfigParser

#-----------------------------------------------------------------------

config = ConfigParser.ConfigParser()
config.read("tetrisrc.conf")

port = int(config.get("configvalues","port"))
dialogbox = bool(config.get("configvalues", "serverdialogbox"))
if dialogbox == True:
    from Tkinter import *
    import tkSimpleDialog
    class RoomNameDialog(tkSimpleDialog.Dialog):
        def __init__(self,parent,room_name,title=None):
            self.room_name = room_name
            tkSimpleDialog.Dialog.__init__(self,parent,title)
        def body(self, master):
            Label(master, text="The room name is: "+self.room_name).grid(row=0)

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
			chatLog.append(line) # Keep track of all the chat messages ever received

			print line

			blastMessage(line, self) # Send out new message to all connected clients

		inFlo.close()
		self._sock.close()
		print 'Closed socket'
		print 'Exiting thread'

		connectionThreads.remove(self) # Remove self from the list of threads

	def sendMsg(self, message):
		outFlo = self._sock.makefile(mode='w')
		outFlo.write(message + "\n")
		outFlo.close()

#-----------------------------------------------------------------------
def blastMessage(newMsg, exceptThread):
	for client in connectionThreads:
		if client != exceptThread:
			client.sendMsg(newMsg)

def main(argv):
    myIP = iputils.getMyIP()
    room_name = iputils.ipToWords(myIP)
    print "Room name:", room_name
    if dialogbox == True:
        root = Tk()
        d = RoomNameDialog(root, room_name, "Room Name")
        root.destroy()
	
    try:
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
			serverThread.sendMsg("Welcome to the LAN party!")
			connectionThreads.append(serverThread) # Add thread to list
    
    except Exception, e:
        print e

#-----------------------------------------------------------------------

if __name__ == '__main__':
	main(argv)
