import requests
from bs4 import BeautifulSoup

page = requests.get("https://twitter.com/FoxNews")
soup = BeautifulSoup(page.content, "html.parser")

bio = soup.select_one(".ProfileHeaderCard-bio")
print(bio.get_text())
