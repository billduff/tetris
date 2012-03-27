import json

def isDict(d):
	try:
		json.loads(d)
	except:
		return False
	return True

def jsonToDict(d):
	return json.loads(jsontext, object_hook=unicodeToASCII)

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

