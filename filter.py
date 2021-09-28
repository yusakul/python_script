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
		emails = open("./EX_EMAILS.txt","a", encoding='utf-8')
		data = fileReader(self.file)
		data=data.decode('utf-8')#python3
		ex_emails= list(set(re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', data)))
		
		for email in ex_emails:
			if len(email) < 2:
				pass
			else:
				emails.write(email.strip()+"\n")

	def urlsEX(self):
		urls = open("./EX_URLS.txt","a", encoding='utf-8')
		data = fileReader(self.file)
		data=data.decode('utf-8')#python3
		ex_urls = list(set(re.findall(r'(?:https?|ftp):\/\/[\w/\-?=%.]+\.[\w/\-?=%.]+', data)))
		for url in ex_urls:
			if len(url) < 2:
				pass
			else:
				urls.write(url.strip()+"\n")

	def hostEX(self):
		urls = open("./EX_Hosts.txt","a", encoding='utf-8')
		data = fileReader(self.file)
		data=data.decode('utf-8')#python3
		ex_urls = list(set(re.findall(r'(?:https?|ftp):\/\/[\w/\-?=%.]+\.[\w/\-?=%.]+', data)))
		for url in ex_urls:
			if len(url) < 2:
				pass
			else:
				reobj = re.compile(r"""(?xi)\A
				[a-z][a-z0-9+\-.]*://								# Scheme
				([a-z0-9\-._~%!$&'()*+,;=]+@)?					   # User
				([a-z0-9\-._~%]+									 # Named or IPv4 host
				|\[[a-z0-9\-._~%!$&'()*+,;=:]+\])					# IPv6+ host
				""")
				match = reobj.search(url)
				if match:
					urls.write(match.group(2).strip()+"\n")



	def ipsEX(self):
		ips = open("./EX_IPS.txt","a", encoding='utf-8')
		data = fileReader(self.file)
		data=data.decode('utf-8')#python3
		ex_ips = list(set(re.findall(r'\b(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b', data)))
		#ex_ips += list(set(re.findall(r'\b(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b', data)))
		
		for ip in ex_ips:
			if validate_ip(ip):
				ips.write(ip.strip()+"\n")

	def MD5EX(self):
		md5s = open("./EX_MD5.txt","a", encoding='utf-8')
		data = fileReader(self.file)
		data=data.decode('utf-8')#python3
		ex_hash = list(set(re.findall(r'(?i)(?<![a-z0-9])[a-f0-9]{32}(?![a-z0-9])', data)))
		
		for index in ex_hash:
			md5s.write(index.strip()+"\n")

	def SHA1EX(self):
		sha1s = open("./EX_sha1.txt","a", encoding='utf-8')
		data = fileReader(self.file)
		data=data.decode('utf-8')#python3
		ex_hash = list(set(re.findall(r'(?i)(?<![a-z0-9])[a-f0-9]{40}(?![a-z0-9])', data)))
		
		for index in ex_hash:
			sha1s.write(index.strip()+"\n")

	def SHA256EX(self):
		sha256s = open("./EX_sha256.txt","a", encoding='utf-8')
		data = fileReader(self.file)
		data=data.decode('utf-8')#python3
		ex_hash = list(set(re.findall(r'(?i)(?<![a-z0-9])[a-f0-9]{64}(?![a-z0-9])', data)))
		
		for index in ex_hash:
			sha256s.write(index.strip()+"\n")

	#自定义的字段
	def interes_files(self):
		int_files = open("./EX_DATA.txt","a", encoding='utf-8')
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
		#EX.emailEX()
		EX.ipsEX()
		#EX.interes_files()
		EX.MD5EX()
		EX.SHA1EX()
		EX.SHA256EX()
		EX.hostEX()
