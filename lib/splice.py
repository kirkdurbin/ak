#this module is used for adding payloads to cloned pages

from BeautifulSoup import BeautifulSoup

def strip(html):
	#strip <head> and <body> tags from html
	x = str(html)
	x = x.replace("<head>", "")
	x = x.replace("</head>", "")
	x = x.replace("<body>", "")
	x = x.replace("</body>", "")
	return x

def splice(html, payload):
	#splice the head and body of two pages together
	#if the payload is not a valid complete html document
	#i.e. payload does not have <html>, <head>, <body>
	#then it just appends payload to html
	try:
		htmlsoup = BeautifulSoup(html)
		payloadsoup = BeautifulSoup(payload)
		htmlbody = strip(htmlsoup.find('body'))
		payloadbody = strip(payloadsoup.find('body'))
		htmlhead = strip(htmlsoup.find('head'))
		payloadhead = strip(payloadsoup.find('head'))
		newbody = "<body>\n" + htmlbody + "\n" + payloadbody + "\n</body>\n"
		newhead = "<head>\n" + htmlhead + "\n" + payloadhead + "\n</head>\n"
		htmlsoup.body = newbody
		htmlsoup.head = newhead
		print "Payload type: PARSED"
		return str(htmlsoup)
	except Exception, err:
		print "Payload type: APPENDED"
		return html + "\n" + payload
