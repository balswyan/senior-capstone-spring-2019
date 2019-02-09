#Using AllSide JSON data return the rating for an inputed website

import json

with open("allsides_data.json") as a:
	news = json.loads(a.read())

for website in news['allside']:

	#if "brucebraley" in website['url']:
		#print(website['bias_rating'])
		
	print(website['url'] + ". Rating:" + website['bias_rating'])