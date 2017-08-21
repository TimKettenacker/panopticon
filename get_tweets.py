

import tweepy
from tweepy import OAuthHandler
consumer_key = 'secret'
consumer_secret = 'secret'
access_token = 'secret'
access_secret = 'secret'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

## to get a glimpse on what the api can do: help(tweepy.API)

## pick an event that arouses controversy atm
## limit the retrieved tweets, otherwise you risk running into status code 429!

import json, os
os.chdir('/Users/timkettenacker/dsproj_repos/python/panopticon')

for tweet in tweepy.Cursor(api.search, q='charlottesville', lang ='de', locale ='de',
                result_type="recent", show_user=True, include_entities=True).items(50):
                with io.open('tweets.json', 'a+', encoding='utf-8') as f:
                    f.write(json.dumps(tweet._json, ensure_ascii=False))

# add {"items": [{ to the beginning of the file, as well as ]} to its end.
# also, replace all occurrences of "result_type": "recent"}} {"contributors" with "result_type": "recent"}}, {"contributors" to split by comma
# and finally, push to neo4j
WITH "file:///Users/timkettenacker/dsproj_repos/python/panopticon/tweets.json" AS url
CALL apoc.load.json(url) YIELD value
UNWIND value.items AS items
RETURN items.text, items.user.screen_name, items.quoted_status_id_str, items.in_reply_to_user_id_str, items.place.full_name

# to get the tweet structure visit https://dev.twitter.com/overview/api/tweets to retrieve further information

# to-do: extract more info from e.g. tweepy status obj and use as input for querying via the API, e.g. get all followers and map them in neo4j
# extract info from tweepy status obj
# dir(tweet)
# tweet.user.id
# api.get_user(id="4760760941")
# for follower in tweepy.Cursor(api.followers_ids, id="4760760941").items():
#     print follower
