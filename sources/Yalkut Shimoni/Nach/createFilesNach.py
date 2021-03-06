# -*- coding: utf-8 -*-
import urllib
import urllib2
from urllib2 import URLError, HTTPError
import json 
import pdb
import os
import sys
from bs4 import BeautifulSoup
import re
p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, p)
os.environ['DJANGO_SETTINGS_MODULE'] = "sefaria.settings"
from local_settings import *

sys.path.insert(0, SEFARIA_PROJECT_PATH)

from sefaria.model import *
parshiot = ["joshua", "sefershoftim", "yishayahu", "yermiyahu", "yehezkel", "tehilim", "mishli", 
"iyob", "shir", "ruth", "eicha", "kohelet", "ester", "daniel", "ezra", "nehemia"]

actual_spellings = ["Joshua", "Judges", "Isaiah", "Jeremiah", "Ezekiel", "Psalms", "Proverbs",
"Job", "Song of Songs", "Ruth", "Lamentations", "Ecclesiastes", "Esther", "Daniel", "Ezra", "Nehemiah"]


for parsha_count, parsha in enumerate(parshiot):
	html = urllib.urlopen("http://www.tsel.org/torah/yalkutsh/"+parsha+".html")
	html_text = str(BeautifulSoup((html.read())))
	text_arr = html_text.split("""<h1""")
	actual_text = ""
	for count, part in enumerate(text_arr):
		if count==0:
			continue
		if count==len(text_arr)-1:
			last_text = text_arr[count].split("</b></font>")
			if len(last_text) == 1:
				print "didnt find b font"
				pdb.set_trace()
			else:
				actual_text += "<h1"+last_text[0]
		else:
			actual_text += "<h1"+text_arr[count]
		
	actual_text = actual_text.replace("<!---mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm-->", "")	
	if os.path.exists(actual_spellings[parsha_count]+".txt") == True:
		os.remove(actual_spellings[parsha_count]+".txt")	
	f = open(actual_spellings[parsha_count]+".txt", "w")
	actual_text = actual_text.replace("</p>", "")
	actual_text = actual_text.replace("<p>", "\n")
	f.write(actual_text)
	f.close()