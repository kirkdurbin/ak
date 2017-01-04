#module to serve cloned websites based on useragent

import BaseHTTPServer
import datetime

for_megacorps = ""
for_normies = ""
auto_blacklist = True

def blacklist(ip):
	ip_fd = open("conf/ip.cnf", "r")
	ips = ip_fd.read().splitlines()
	ip_fd.close()
	unique = True
	for x in ips:
		if ip == x:
			unique = False
	if unique:
		print "Based on user agent, " + ip + " was added to the IP blacklist."
		black_fd = open("conf/ip.cnf", "a")
		black_fd.write(ip + "\n")
		black_fd.close()

def serve(useragent, address):
	global for_megacorps
	global for_normies
	#check if client address is blacklisted
	ip_fd = open("conf/ip.cnf", "r")
	ips = ip_fd.read().splitlines()
	ip_fd.close()
	for ip in ips:
		if address == ip:
			return [for_megacorps, True]
	#if ip not matched, check for blacklisted user agent
	if useragent == None:
		return for_normies
	corp_fd = open("conf/ua.cnf", "r")
	corp_agents = corp_fd.read().splitlines()
	corp_fd.close()
	corp = False
	for agent in corp_agents:
		if useragent in agent:
			if auto_blacklist:
				blacklist(address)
			corp = True
	if corp:
		return [for_megacorps, True]
	else:
		return [for_normies, False]

class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(s):
		ip = s.client_address[0]
		ua = s.headers.get('User-Agent')
		to_serve = serve(ua, ip)
		html = to_serve[0]
		if to_serve[1]:
			try:
				print ip + " is being served the blacklist content. [" + ua + "]"
			except:
				print ip + " is being served the blacklist content."
		else:
			try:
				print ip + " is being served the normal content. [" + ua + "]"
			except:
				print ip + " is being served the normal content."
		log = open("access.log", "a")
		log.write(ip + " | Blacklist: " + str(to_serve[1]) + " | " + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + "\n")
		log.close()
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		s.wfile.write(html)

def webserver(corp_html, normie_html, ftp):
	global for_megacorps
	global for_normies
	global auto_blacklist
	for_megacorps = corp_html
	for_normies = normie_html
	auto_blacklist = ftp
	host = '0.0.0.0'
	port = 80
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((host, port), HTTPHandler)
	try:
		httpd.serve_forever()
	except:
		pass
	httpd.server_close()
