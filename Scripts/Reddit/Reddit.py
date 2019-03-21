import json
import requests

def get_url_info(url):
    """
    To pull the information/text in a html file.

    :param html_file (string): name of an html file to process.

    :return html_info (dict): the basic information in the html file.
    """
    data = _get_request(url + '.json')
    data = _get_submission_object(data)

    title = data['title']
    description = data['subreddit']
    paragraphs = data['selftext'] #Post text as the paragraph 

    if len(paragraphs) == 0: #No post text, might be a URL or AskReddit type thread(just title)
        paragraphs = data['url']
        if data['id'] in paragraphs: #Check to see if the URL is just the post URL
            paragraphs = '' #Post is just the title, probably an AskReddit type thread

    images = ''
    if data['media']: #Media post, save the media in the images portion
        images = data['url'] #Media posts have the media in the URL section

    html_info = {
        'title': title,
        'description': description,
        'paragraphs': paragraphs,
        'images': images
    }
    return html_info


def _get_submission_object(data):
    """
    Returns the JSON object related to the submission
    """
    return data[0]["data"]["children"][0]["data"]
    
def _get_request(url):
    """
    Returns HTML of given URL
    
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0'
    }
    req = requests.get(url, headers=headers)
    return json.loads(req.text)
