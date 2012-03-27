#Use isJSON to check if a given string is a JSON string and can be converted to a dict
#Use jsonToDict to convert a JSON string to an actual dict-- this is better than plain json.loads()
#To convert a dict to json, you don't need this library; just use json.dumps(yourdictionary)

###EXAMPLE CODE:
#mydict = {"foo":8,"bar":10}
#mydictstr = json.dumps(mydict)
#if isJSON(mydictstr):
#    mydict = jsonToDict(mydictstr)

import json

def isJSON(d):
	try:
		json.loads(d)
	except:
		return False
	return True

def jsonToDict(d):
	return json.loads(d, object_hook=unicodeToASCII)

#By default, every string that json.loads() returns is in Unicode format. 
#This can cause problems, so this function converts every Unicode object back to a string, recursively through the dict.
def unicodeToASCII(x):
	if isinstance(x,dict):
		newdict = {}
		for term in x:
			newdict[str(term.encode('ascii','replace'))] = unicodeToASCII(x[term])
		x = newdict
	elif isinstance(x,list):
		for i in xrange(len(x)):
			x[i] = unicodeToASCII(x[i])
	elif isinstance(x,unicode):
		x = x.encode('ascii','replace')
	return x
