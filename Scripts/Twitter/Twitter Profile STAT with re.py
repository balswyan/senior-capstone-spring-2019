from cookielib import CookieJar
import requests
import urllib2
import os
import re
import time

cookies = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 '
                                    '(KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]		
#if link is tweets urls: 
def stat_lookup():
	profile_path ='https://twitter.com/FoxNews'
	source = opener.open(profile_path).read()
	findLables = re.findall(r'<div class="statlabel"> (.*?) </div>', source)
	findNumbers = re.findall(r'<div class="statnum">(.*?)</div>', source)
	
	#for findLable in findLables:
	print(findLables) #print(findLable)
	
	#for findNumber in findNumbers:
	print(findNumbers) #print(findNumber)
stat_lookup()
