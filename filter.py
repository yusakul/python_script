# -*- coding: utf-8 -*
import os,sys
import re


path = sys.argv[1]


sourcesList = []

def fileReader(file):
	f = open(file,"rb").read()
	return f

def Lister(path):
	for fpath, dirs,files in os.walk(path):
		for file in files:
			sourcesList.append(os.path.join(fpath, file))
				
				
def validate_ip(ip):
	if ":" in ip:
		ip = ip.split(":")[0]
	m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
	return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))



Lister(path)

print("[+] Sources list successfully generated !")

class Extractor:
	def __init__(self,file):
		self.file = file

	def emailEX(self):
		emails = open("./EX_EMAILS.txt","a")
		data = fileReader(self.file)
		data=data.decode('utf-8')#python3
		ex_emails= list(set(re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', data)))
		
		for email in ex_emails:
                        if len(email) < 2:
                                pass
                        else:
                                emails.write(email.strip()+"\n")

	def urlsEX(self):
		urls = open("./EX_URLS.txt","a")
		data = fileReader(self.file)
		data=data.decode('utf-8')#python3
		ex_urls = list(set(re.findall(r'(?:https?|ftp):\/\/[\w/\-?=%.]+\.[\w/\-?=%.]+', data)))
		for url in ex_urls:
			if len(url) < 2:
				pass
			else:
				urls.write(url.strip()+"\n")

	def ipsEX(self):
		ips = open("./EX_IPS.txt","a")
		data = fileReader(self.file)
		data=data.decode('utf-8')#python3
                ex_ips = list(set(re.findall(r'\b(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b', data)))
		#ex_ips += list(set(re.findall(r'\b(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b', data)))
		
		for ip in ex_ips:
			if validate_ip(ip):
				ips.write(ip.strip()+"\n")

	#自定义的字段
	def interes_files(self):
		int_files = open("./EX_DATA.txt","a")
		words = open("filter_custom.lst","r").read()
		data = fileReader(self.file)
		for word in words.split("\n"):
			if len(word) >= 2:
				if word.upper() in data or word.lower() in data or word in data:
					int_files.write("{} \t: {}\n".format(word,self.file))

if __name__ == '__main__':
	for sl in sourcesList:
		EX = Extractor(sl)
		EX.urlsEX()
		EX.emailEX()
		EX.ipsEX()
		EX.interes_files()
