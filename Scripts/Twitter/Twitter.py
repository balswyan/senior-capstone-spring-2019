import tweepy
import pickle
import json


def get_url_info(tweet_id, input_path):
    try:
        api = _connect_to_twitter_api(input_path, 'key.p')
        tweet = api.get_status(tweet_id, tweet_mode='extended')
        
        tweet_text = tweet.full_text
        user_bio = tweet.user.description

        images = []
        for media in tweet.extended_entities["media"]:
            if media['type'] == 'photo':
                    images.append(media['media_url'])
        
        tweet_info = {
            "title": tweet_text,
            "description": user_bio,
            "paragraphs": "",
            "images": images,
        }
        return tweet_info
    except tweepy.TweepError as error:
        return error.reason

def _connect_to_twitter_api(keys_path, key_name):
    """
    This function connets to the Twitter API via tweepy and returns an API
    object.
    
    'keys_path' = (string)  Path where your key is located
    'key_name' = (string)   Name of the key object. Pickle file containing a
                            dictionary with the following keys: 'ckey', 
                            'csecret', 'atoken', and 'asecret'.
    """
    # - import pickle file with the key
    key = pickle.load(open('%s%s' % (keys_path, key_name), 'rb'))
    auth = tweepy.OAuthHandler(key['ckey'], key['csecret'])
    auth.set_access_token(key['atoken'], key['asecret'])
    api = tweepy.API(auth)
    return(api)
