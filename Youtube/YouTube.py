from bs4 import BeautifulSoup
import re
import os
import json

def main():
    with open('Page.html', 'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    data = _get_json(soup)
    get_youtube_info(data)

def get_youtube_info(json_data):
    #Title, Views
    videoPrimaryInfoRenderer = json_data[0]["videoPrimaryInfoRenderer"]
    video_title = videoPrimaryInfoRenderer["title"]["simpleText"]
    view_count = videoPrimaryInfoRenderer["viewCount"]["videoViewCountRenderer"]["viewCount"]["simpleText"]
    view_count_clean = _strip_non_numeric(view_count)

    #Likes, Dislikes
    topLevelButtons = videoPrimaryInfoRenderer["videoActions"]["menuRenderer"]["topLevelButtons"]
    likes_count = topLevelButtons[0]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"]
    likes_count_clean = _strip_non_numeric(likes_count)

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

    html_info = {
        'title':video_title,
        'views':view_count_clean,
        'likes':likes_count_clean,
        'dislikes':dislikes_count_clean,
        'channel_name:':channel_name,
        'channel_id:':channel_id,
        'subscriber_count':subscriber_count_clean,
        'description':description,
        'categories':categories
        }
    return html_info
    
    




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