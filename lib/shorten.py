#get your external ip and attempt to shorten it with goo.gl

import urllib2

def get_ip(count=0):
	if count < 3:
		try:
			ip = urllib2.urlopen("http://myexternalip.com/raw").read()
			return ip.replace("\n", "")
		except:
			print "Failed to get external IP! Retrying up to " + str(3-count-1) + " more times..."
			return get_ip(count+1)
	else:
		print "Giving up on getting external IP."
		return ip


def shorten_keyless():
	url = "http://" + get_ip()
	data = "{\"longUrl\": \"" + url + "\"}"
	req = urllib2.Request("https://www.googleapis.com/urlshortener/v1/url", data, {'Content-Type': 'application/json'})
	try:
		response = urllib2.urlopen(req).read()
		lines = response.splitlines()
		for line in lines:
			if "id" in line:
				link = line.split(": \"")[1][:-2]
				return link
		return None
	except:
		#error 403
		return None

def shorten_key(key):
	url = "http://" + get_ip()
	data = "{\"longUrl\": \"" + url + "\"}"
	googl_url = "https://www.googleapis.com/urlshortener/v1/url?key=" + key
	req = urllib2.Request(googl_url, data, {'Content-Type': 'application/json'})
	try:
		response = urllib2.urlopen(req).read()
		lines = response.splitlines()
		for line in lines:
			if "id" in line:
				link = line.split(": \"")[1][:-2]
				return link
		return None
	except:
		#error 403
		return None

def shorten(key=""):
	link = shorten_keyless()
	if link == None:
		link = shorten_key(key)
	if link == None:
		print "[?] Could not shorten link."
		link = "http://" + get_ip()
	return link
