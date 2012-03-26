import urllib #needed for getMyIP function

f = open("wordlist.txt")
ipwords = f.read()
f.close()

ipwords = ipwords.split(",") 

def getMyIP():
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

def ipToWords(ip):
	ipstr = ""
	for i in ip:
		ipstr += ipwords[i] + " "
	ipstr = ipstr[:-1] #remove trailing space
	return ipstr

def wordsToIP(ipstr):
	ip = []
	for ipword in ipstr.split(' '):
		i = 0
		wordguess = ipwords[i]
		while wordguess != ipword:
			i += 1
			ipword = ipwords[i]
		ip.append(i)
	return ip
