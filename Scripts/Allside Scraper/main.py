import urllib2
from cookielib import CookieJar
import os
import re
import time


cookies = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 '
                                    '(KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]


def news_lookup():
	news_path = 'https://www.allsides.com/media-bias/media-bias-ratings?field_featured_bias_rating_value=All&page=2'
	source = opener.open(news_path).read()
	findLinks = re.findall(r'href="/news-source/(.*?)">', source)
	for eachThing in findLinks:
		linkPath = 'https://www.allsides.com/news-source/' + eachThing
		source2 = opener.open(linkPath).read()
		findNews = re.findall(r'<a href="(.*?) " title=', source2)
		findName = re.findall(r'property="og:title" content="(.*?)" />', source2)
		#print(findName)
		#print(findNews)
		print(linkPath)

news_lookup()


