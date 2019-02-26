import requests
import re
import os
import time
import json
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import xml.etree.ElementTree as ET


def main():
    with open('Scripts/Youtube/Page2.html', 'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    get_youtube_info(soup)
	
def get_youtube_info(html_soup):
    json_data = _get_json(html_soup)

    #Title, Views
    videoPrimaryInfoRenderer = json_data[0]["videoPrimaryInfoRenderer"]
    video_title = videoPrimaryInfoRenderer["title"]["simpleText"]
    view_count = videoPrimaryInfoRenderer["viewCount"]["videoViewCountRenderer"]["viewCount"]["simpleText"]
    view_count_clean = _strip_non_numeric(view_count)

    #Likes, Dislikes
    topLevelButtons = videoPrimaryInfoRenderer["videoActions"]["menuRenderer"]["topLevelButtons"]
    likes_count = topLevelButtons[0]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"]

    dislikes_count = topLevelButtons[1]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"]
    dislikes_count_clean = _strip_non_numeric(dislikes_count)

    #Channel Name, Channel ID, Subscriber Count
    videoSecondaryInfoRenderer = json_data[1]["videoSecondaryInfoRenderer"]
    videoOwnerRender = videoSecondaryInfoRenderer["owner"]["videoOwnerRenderer"]
    channel_name = videoOwnerRender["title"]["runs"][0]["text"]
    channel_id = videoOwnerRender["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
    subscriber_count = videoOwnerRender["subscriberCountText"]["simpleText"]
    subscriber_count_clean = _strip_non_numeric(subscriber_count)
	
	#Description
    description_runs = videoSecondaryInfoRenderer["description"]["runs"]
    description = ""     
    for text in description_runs:
        description += text["text"]
    description = description.replace('\n', '\t') #TODO change from \t to something more consistent
    
    #Category
    category_runs = videoSecondaryInfoRenderer["metadataRowContainer"]["metadataRowContainerRenderer"]["rows"][0]["metadataRowRenderer"]["contents"][0]["runs"]
    categories = [cat["text"] for cat in category_runs]
    
	#Channel description
    channel_desc = description_lookup(channel_name)

    #Captions
    caption = caption_parser(html_soup)
    likes_count_clean = _strip_non_numeric(likes_count)

    html_info = {
        'title':video_title,
        'views':view_count_clean,
        'likes':likes_count_clean,
        'dislikes':dislikes_count_clean,
        'channel_name:':channel_name,
        'channel_id:':channel_id,			
        'subscriber_count':subscriber_count_clean,
        'description':description,
        'channel_description':channel_desc,
        'caption':caption,
        'categories':categories
        }
    return html_info

def caption_parser(html_soup):
    caption_url = ''
    caption_re = re.search(r'timedtext[?](.*?)"', html_soup.text)
    if caption_re is not None:
        caption_url = caption_re.group(1).replace("\\\\u0026", "&").replace("%2C",",").replace("\\", "")
    else: #No captions found
        return None
    
    caption_url = "https://youtube.com/api/timedtext?" + caption_url
    xml = _get_request(caption_url)

    caption_text = ''
    hparser = HTMLParser()
    xml = BeautifulSoup(xml, features='lxml')

    xml = xml.findAll(text=True)
    for piece in xml:
        caption_text += re.sub(r'<font color=\"(.*?)\">', '', piece).replace('</font>', '') + " "
    caption_text = caption_text.replace('xml version="1.0" encoding="utf-8" ?', '')
    caption_text = hparser.unescape(caption_text)
    
    return caption_text

def description_lookup(channel_name):
    """
    Returns the description of given channel
    
    :param channel_name (string): Channel ID/name
    
    :return channel_desc (string): Channel description
    """
    html = _get_request('https://youtube.com/' + channel_name + '/about')
    channel_desc = re.search(r'description" content="(.*?)"', html)
    if channel_desc is not None:
        return channel_desc.group(1)
    else:
        return None

def _get_request(url):
    """
    Returns HTML of given URL
    
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0'
    }
    req = requests.get(url, headers=headers)
    return req.text

def _strip_non_numeric(item):
    """
    Removes non numeric values from item
    
    :param item (string): the string with non-numeric values
    
    :return clean_text (string): the string without non-numeric values.
    """
    pattern = re.compile(r'[^0-9.]')
    clean_text = re.sub(pattern, "", item)
    return clean_text

def _get_json(html_soup):
    result = re.findall(r'window\["ytInitialData"\] = ({.*?});', html_soup.text)
    data = json.loads(result[0])
    data = data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"]
    return data

if __name__ == "__main__":
    main()    