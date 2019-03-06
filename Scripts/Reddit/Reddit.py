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
	reddit_path = 'https://www.reddit.com/r/AskReddit/comments/axkvja/what_is_a_unique_game_you_played_as_a_child/'
	source = opener.open(reddit_path).read()
	findReddit = re.findall(r': (.*?)</title><meta ', source)
	findTitle = re.findall(r' </script><title>(.*?) : ', source) #need to decode from UTF-8 into Unicode to convert this into a "single" Unicode character base. 
	
	print(findReddit)
	print(findTitle)
stat_lookup()
