import requests
import re
from bs4 import BeautifulSoup
import info

r = requests.get(info.learn_url)
htmltext = BeautifulSoup(r.text, 'html.parser')
course = htmltext.find_all('div', class_ ='info')

x = open("htmloutput.txt", "w")
x.write("begin\n")
x = open("htmloutput.txt", "a")

for i in course:
	#regex to match course id 8 digit identifier
	regexstr = r"\b[\dA-Z]{8}\b"
	if(re.match(regexstr, i.text)):
		x.write(i.text + "\n")


