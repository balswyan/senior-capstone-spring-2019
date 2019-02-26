import requests
from bs4 import BeautifulSoup

page = requests.get("https://twitter.com/CNN/status/1100426848578744322")
soup = BeautifulSoup(page.content, "html.parser")

tweet = soup.select_one(".js-tweet-text-container .TweetTextSize--jumbo")

print(tweet.get_text())

