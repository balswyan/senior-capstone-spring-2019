import requests
from bs4 import BeautifulSoup

page = requests.get("https://twitter.com/FoxNews")
soup = BeautifulSoup(page.content, "html.parser")

#if link is tweets urls:

#tweet = soup.select_one(".js-tweet-text-container .TweetTextSize--jumbo") //this for jumbo tweets urls

#if page is profile: //Need to get stats for that with ProfileNav-value class and ProfileNav-label since it only return the first select

#bio = soup.select_one(".ProfileHeaderCard-bio") //this to grab the bio of the users upon profile link url
#tweetsValue = soup.select_one(".ProfileNav-value") //number of Tweets
#print(tweetsValue.get_text())


#profile_values = soup.select(".ProfileNav-value") //grab all the selects of that class
#profile_labels = soup.select(".ProfileNav-label")
#print profile_labels get the list grouped togther.