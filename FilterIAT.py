# -*- coding: utf-8 -*
import os,sys
import re
import string, shutil,re
import pefile

path = sys.argv[1]


sourcesList = []
NetApiList = ['socket', 'request', 'http']
NetDllList = ['netlib40.dll', 'WS2_32.dll', 'WININET.dll']

def fileReader(file):
	f = open(file,"rb").read()
	return f

def Lister(path):
	for fpath, dirs,files in os.walk(path):
		for file in files:
			if  file.endswith('.exe') or file.endswith('.dll'):
				sourcesList.append(os.path.join(fpath, file))
				
				


Lister(path)

print("[+] Sources list successfully generated !")

class Extractor:
	def __init__(self,file):
		self.file = file

	def iatEX(self):
		iat = open("./EX_IAT.txt","a")
		print(self.file)
		pe = pefile.PE(self.file)

		for importeddll in pe.DIRECTORY_ENTRY_IMPORT:
			#print(importeddll.dll)
			for dll in NetDllList:
				if dll.lower() in str(importeddll.dll).lower():
					iat.write("find dll->  " + self.file+ " : " + str(importeddll.dll) + "\n")
			for importedapi in importeddll.imports:
				# print importedapi.name
				for api in NetApiList:
					if api.lower() in str(importedapi.name).lower():
						iat.write("find api->  " + self.file+ " : " + str(importeddll.dll) + " : " + str(importedapi.name) + "\n")


if __name__ == '__main__':
	for sl in sourcesList:
		EX = Extractor(sl)
		EX.iatEX()
