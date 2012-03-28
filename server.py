#!/usr/bin/env python

#-----------------------------------------------------------------------
# server.py
#-----------------------------------------------------------------------

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import time
import sys
import signal
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
            Label(master, text="The room name will be: "+self.room_name).grid(row=0)
            Label(master, text="Press \"OK\" to start the server.").grid(row=1)

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
        self._inFlo = self._sock.makefile(mode='r')
        while True:
            line = self._inFlo.readline()
            if not line:
                break

            blastMessage(line, self) # Send out new message to all connected clients

        self.quitThread()
        
    def sendMsg(self, message):
        outFlo = self._sock.makefile(mode='w')
        outFlo.write(message + "\n")
        outFlo.close()
        
    def quitThread(self):
        self._inFlo.close()
        self._sock.close()
        print 'Closed socket'        
        connectionThreads.remove(self) # Remove self from the list of threads
        print 'Server thread can exit now...'
        
#-----------------------------------------------------------------------
def blastMessage(newMsg, exceptThread):
    for client in connectionThreads:
        if client != exceptThread:
            client.sendMsg(newMsg)
            
def quitThreads(signal, frame):
    print "Server received ctrl-c"
    for client in connectionThreads:
        client.quitThread()
        print "Quit a server thread..."
        client._Thread__stop()
    print "Quit all threads..."
    sys.exit()

def main():
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

signal.signal(signal.SIGINT, quitThreads)
signal.signal(signal.SIGQUIT, quitThreads)

if __name__ == '__main__':
    main()
