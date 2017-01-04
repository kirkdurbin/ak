#module to clone websites locally

import subprocess
import urlparse

def fetch_site(url, name):
	#fetch external site to clone
	try:
		command = 'cd tmp/; rm -f ' + name + '; wget --no-check-certificate -O ' + name + ' -N -c -k ' + url
		subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
		return True
	except:
		return False

def load_site(path, name):
	#fetch local html to clone
	try:
		fd_in = open(path, "r")
		clone = fd_in.read()
		fd_in.close()
		fd_out = open("tmp/" + name, "w")
		fd_out.write(clone)
		fd_out.close()
		return True
	except Exception, err:
		print str(err)
		return False

def clone_site(location, name):
	x = urlparse.urlparse(location)
	if bool(x.netloc):
		status = fetch_site(location, name)
	else:
		status = load_site(location, name)
	return status
