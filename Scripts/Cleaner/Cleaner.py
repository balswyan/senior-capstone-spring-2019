import pandas as pd

def clean_csv(file, output=None):
    """
    Removes non-relevant URLs from matchUrls CSV
    
    :param file (string): Path to CSV containing URLs

    :param output (string): Path to save cleaned CSV
    
    :return dframe (Pandas Dataframe): Cleaned CSV in the form of a dataframe
    """
    #category, url, people_count
    dframe = pd.read_csv(file, sep=',', low_memory=False)

    url_filter = ['slickdeals.net', 'swagbucks.com', 'shutterstock.com', 'slideshare.net', 'smugmug.com', 'glassdoor.com' , 'indeed.com', 'monster.com', 'ziprecruiter.com', 'upwork.com', 'gfycat.com', 'giphy.com', 'craigslist.com', 'ancestry.com', 'quizlet.com', 'scribd.com', 'coursehero.com', 'chegg.com', 'hbo.com', 'crackle.com', 'sonycrackle.com' ,'metacafe.com', 'slacker.com', 'pandora.com', 'tidal.com', 'spotify.com', 'soundcloud.com', 'vimeo.com', 'netflix.com', 'zillow.com', 'imgur.com' ,'mail.yahoo.com', 'outlook.live.com', 'mail.google.com', 'accounts.google.com', 'myaccount.google.com', 'docs.google.com', 'drive.google.com', 'calendar.google.com', 'play.google.com', 'admin.google.com', 'aboutme.google.com', 'adwords.google.com', 'allo.google.com', 'chrome.google.com', 'classroom.google.com', 'code.google.com', 'cloud.google.com', 'developers.google.com', 'contacts.google.com', 'earth.google.com', 'support.google.com', 'domains.google.com', 'express.google.com', 'hangouts.google.com', 'photos.google.com',  'google.com/mail', 'google.com/search', 'bing.com/search', 'yahoo.com/search', 'google.com/maps', 'messenger.com', 'slack.com', 'proquest.com', 'vitalsource.com', 'jstor.org']
    blacklists = _load_file('data/adult_domains.txt') #http://dsi.ut-capitole.fr/blacklists/index_en.php
    blacklists += _load_file('data/bank_domains.txt')

    dframe = dframe[dframe['url'].str.contains('http|https')] #Only allow URLs with http(s)
    dframe = dframe[~dframe['url'].str.contains('|'.join(url_filter))] #Filter out URLs
    dframe = dframe[~dframe['url'].isin(blacklists)] #Filter out adult and bank

    #dframe.loc[dframe['url'].str.contains('https://www.youtube.com/watch'), 'url'] = dframe['url'].str.split('\&').str.get(0)
    if output is not None:
        dframe.to_csv(output, sep=',', index=False)
    return dframe

def _load_file(file):
    listt = []
    with open(file, "r") as ins:
        for line in ins:
            listt.append(line.strip())
    return listt

#clean_csv('data/matchUrlsFeb19.csv', 'data/filteredUrls.csv')