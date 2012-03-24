import socket
import urllib

class Commlink(object):
	def __init__(self):
		pass
	def getThisIP(self):
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
		
	def connectToIP(self, ip):
		print "This function should connect to a different computer"
	def send(self,ip,message):
		print "This function should send a message to the other IP"
	def poll(self):
		print "This function should get messages from the other computers"

ipWords = []

def ipToWords(ip):
	pass

def wordsToIP(words):
	pass

def testCommlink():
	c = Commlink()
	print "This computer's IP is",c.getThisIP()

testCommlink()
