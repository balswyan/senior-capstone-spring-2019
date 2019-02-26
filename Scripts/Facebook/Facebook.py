from bs4 import BeautifulSoup
import os
import re

def main():
    with open('Scripts/Facebook/Page.html', 'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    print(get_facebook_info(soup))

def get_facebook_info(html_soup):
    html = html_soup.decode()
    post_re = re.search('userContent .*?<p>(.*?)</div>', html)
    if post_re is None: #Can't get post contents(probably not a post then)
        return None
    #author_re = re.search('og:title\" content=\"(.*?)\"', html) #TODO PARSE AUTHOR
    post_text = post_re.group(1).replace('<p>', '').replace('</p>', '')
    #author_text = author_re.group(1)
    html_info = {
        #'author':author_text,
        'post':post_text
    }
    return html_info

main()

    