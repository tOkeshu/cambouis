import requests
import json

URL = "https://stream.twitter.com/1.1/statuses/filter.json"
KEYWORDS = ['keyword']
USERNAME = "user"
PASSWORD = "password"

class Tweet(object):

    def __init__(self, user, status, permalink):
        self.user = user
        self.status = status
        self.permalink = permalink

def firehose():
    r = requests.post(URL, data={'track': ','.join(KEYWORDS)},
                      auth=(USERNAME, PASSWORD),
                      stream=True)
    for line in r.iter_lines():
        if line: # filter out keep-alive new lines
            tweet = json.loads(line)
            retweet = tweet.get('retweeted_status', None)
            tweet = (retweet or tweet)

            user = tweet['user']['screen_name']
            status = tweet['text']
            permalink = 'https://twitter.com/%s/statuses/%s' % (user, tweet['id'])

            yield Tweet(user, status, permalink)

