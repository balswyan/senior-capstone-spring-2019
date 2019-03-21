import re
from bs4 import BeautifulSoup

def get_url_info(html_soup):

    title = html_soup.find_all('title')
    if len(title) > 0:
        title_clean = _clean_html(str(title[0]))
    else:
        title_clean = ''
    
    bio = html_soup.select_one(".ProfileHeaderCard-bio").get_text()
    tweet = html_soup.select_one(".js-tweet-text-container .TweetTextSize--jumbo").get_text()
    html_info = {
        'title': title_clean,
        'description': bio,
        'paragraphs': tweet
        #'images': images
    }
    return html_info


def _clean_html(raw_html_string):
    """
    To remove html tags from strings.
    
    :param raw_html_string (string): the string with html tags.
    
    :return clean_html_string (string): the string without html tags.
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html_string).decode('utf-8', 'ignore').encode('ascii', 'ignore') # Helps with encoding issues on RT and WashPost
    return cleantext
