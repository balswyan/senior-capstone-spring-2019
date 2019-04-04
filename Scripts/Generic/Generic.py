import argparse
from bs4 import BeautifulSoup
import re
import os
import urllib
import json

#https://github.com/codelucas/newspaper
def main():
    print(os.getcwd())
    output_path = 'Scripts/Generic/'
    html_info = get_url_info('Page.html', output_path)
    json.dump(html_info, open('%s/%s.json' % (output_path, "Page"), 'w'))

def get_url_info(html_file, input_path):
    """
    To pull the information/text in a html file.
    
    :param html_file (string): name of an html file to process.
    
    :return html_info (dict): the basic information in the html file.
    """
    # - load the html file
    with open('%s/%s' % (input_path, html_file), 'r') as infile:
        html = infile.read()

    # - pull the relevant information
    # ... Title
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find_all('title')
    if len(title) > 0:
        title_clean = _clean_html(str(title[0]))
    else:
        title_clean = ''
    # ... Description
    description = soup.find_all(itemprop="description")
    if len(description) == 0:
        # - try finding a description using other tags
        description = soup.find_all('meta', {'name': 'description'})
    if len(description) > 0:
        # - try pulling the description by removing html tags
        description_clean = _clean_html(str(description[0]))
        if len(description_clean) == 0:
            # - try pulling the description from within the html tag
            description_clean = _clean_inside_html_tag(str(description[0]))
    else:
        description_clean = ''
    # ... Paragraphs
    paragraphs = soup.find_all('p')
    if len(paragraphs) > 0:
        paragraphs_clean = [_clean_html(str(p)) for p in paragraphs]
        paragraphs_clean = [x for x in paragraphs_clean if x != '']
    else:
        paragraphs_clean = []
    # ... Main image followed by the other images
    images = soup.find_all(itemprop="image")
    more_images = soup.find_all('img')
    all_images = images + more_images
    if len(all_images) > 0:
        images_clean = [_get_image_url(str(x)) for x in all_images]
        # ... ignore images that are not jpg or jpeg (are likely banners etc.)
        images_clean = [x for x in images_clean if 'jpg'
                        in x or 'jpeg' in x]
    else:
        images_clean = []
    images_clean_dedup = _unique_list(images_clean)
    html_info = {
        'title': title_clean,
        'description': description_clean,
        'paragraphs': paragraphs_clean,
        'images': images_clean_dedup
    }
    return html_info


def _clean_html(raw_html_string):
    """
    To remove html tags from strings.
    
    :param raw_html_string (string): the string with html tags.
    
    :return clean_html_string (string): the string without html tags.
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html_string).decode(
        'utf-8', 'ignore').encode('ascii', 'ignore')  # Helps with encoding issues on RT and WashPost
    return cleantext


def _clean_inside_html_tag(raw_html_string):
    """
    To pull text from within html tags.
    
    :param raw_html_string (string): the html tag with text in it
    
    :return clean_html_string (string): the string without html tags.
    """
    actual_text = re.compile(r'"([^"]*)"')
    clean_text = re.findall(actual_text, raw_html_string)[0]
    return clean_text


def _get_image_url(raw_html_string):
    """
    To get the image url link from an image html element
    
    :param raw_html_string (string): the string with the html image tag.
    
    :return image_url (string): the url/link to the image
    """
    new_raw = re.findall('(?P<url>https?://[^\s]+)', raw_html_string)
    if len(new_raw) > 0:
        # - get rid of anything after the .jpg/.jpeg ending
        new_raw_str = str(new_raw[0])
        if '.jpg' in new_raw_str:
            last_i = new_raw_str.index('.jpg') + 4
            image_url = new_raw_str[:last_i]
        elif '.jpeg' in new_raw_str:
            last_i = new_raw_str.index('.jpeg') + 5
            image_url = new_raw_str[:last_i]
        else:
            image_url = new_raw_str
    else:
        image_url = ''
    return(image_url)


def _unique_list(any_list):
    """
    To remove duplicates from a list while keeping the order.
    
    :param any_list (list): the list the de-duplicate.
    
    :return deduplicated_list (list): output list with no duplicates.
    """
    seen = set()
    seen_add = seen.add
    new_list = [x for x in any_list if not (x in seen or seen_add(x))]
    return new_list


if __name__ == "__main__":
    main()
