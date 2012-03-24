import socket
import urllib
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("tetrisrc.conf")

port = int(config.get("configvalues","port"))

class Commlink(object):
	def __init__(self):
		self.myip = self.getMyIP()
		self.availableForConnections()

	def getMyIP(self):
		webserviceurl = "http://automation.whatismyip.com/n09230945.asp" #HTTP GET request to this URL returns the public IP address
		try:
			webpageobj = urllib.urlopen(webserviceurl)
			ipaddr = webpageobj.read()
			webpageobj.close()
		except:
			raise Exception, "Could not connect to internet to find this computer's IP address!"
		if ipaddr.count(".") != 3:
			raise Exception, "Malformed IP address retrieved from internet"
		ipaddr = ipaddr.split(".")
		ipaddr = [int(i) for i in ipaddr]
		return ipaddr
	
	def availableForConnections(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(("",port))
		s.listen(1)
		print "Listening for connections..."
		conn, addr = s.accept() #this code blocks! use threading to get around it later
		print "Connected by",addr
		while True:
			data = conn.recv(1024)
			if not data: break
			conn.send("OK")
		conn.close()
		#self.connectedusers = []

	def connectToIP(self, ip):
		print "This function should connect to a different computer"
	
	def send(self,ip,message):
		print "This function should send a message to the other IP"
        #change to take list of messages?
	
	def poll(self):
		print "This function should get messages from the other computers"
        #Make sure this gets the players in the same order every time.
        #Should return a list of messages

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

def testCommlink():
	c = Commlink()
	ip = c.myip
	print "This computer's IP is",ip
	ipstr = ipToWords(ip)
	print "This computer's IP Name is",ipstr
	print "The computer will connect on port",port

testCommlink()
