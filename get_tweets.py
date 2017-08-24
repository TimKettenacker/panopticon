
import tweepy
from tweepy import OAuthHandler
consumer_key = 'secret'
consumer_secret = 'secret'
access_token = 'secret'
access_secret = 'secret'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

## pick an event that arouses controversy atm
## limit the retrieved tweets, otherwise you risk running into status code 429!

import json, os, io
os.chdir('/Users/timkettenacker/dsproj_repos/python/panopticon')

for tweet in tweepy.Cursor(api.search, q='charlottesville', lang ='de', locale ='de',
                result_type="recent", show_user=True, include_entities=True).items(50):
                with io.open('tweets.json', 'a+', encoding='utf-8') as f:
                    f.write(json.dumps(tweet._json, ensure_ascii=False))

# add {"items": [{ to the beginning of the file, as well as ]} to its end.
# also, replace all occurrences of "result_type": "recent"}} {"contributors" with "result_type": "recent"}}, {"contributors" to split by comma
# and finally, use the apoc loading procedure from within the cypher terminal of neo4j to push data to the database
# (of course, this is also possible from within neo4j)

WITH "file:///Users/timkettenacker/dsproj_repos/python/panopticon/tweets.json" AS url
CALL apoc.load.json(url) YIELD value
UNWIND value.items AS items
MERGE (tweeter:Tweeter {id:items.user.id}) ON CREATE
  SET tweeter.name = items.user.screen_name, tweeter.followers = items.user.follower_count, tweeter.description = items.user.description
  MERGE (tweet:Tweet {id:items.id_str}) ON CREATE SET tweet.text = items.text, tweet.replied_status = items.quoted_status_id_str,
  tweet.replied_tweet = items.in_reply_to_user_id_str, tweet.location = items.place.full_name
  MERGE (tweeter)-[:tweets]->(tweet)

# it's time to retrieve the followers of every tweeter and update their relationship accordingly
# to get the tweet structure visit https://dev.twitter.com/overview/api/tweets to retrieve further information

import py2neo
from py2neo import authenticate, Graph
authenticate('localhost:7474', 'neo4j', 'root')
graph = Graph('http://localhost:7474/db/data')

for tweeter in  graph.run('MATCH (t:Tweeter) RETURN t'):
    user_follows_list = api.friends_ids(tweeter[0]['id'])
    for user_follow in user_follows_list:
        follow = api.get_user(user_follow)
        try:
            add_follow2db = graph.run("MERGE (tweeter:Tweeter {id:" + follow.id_str + "}) ON CREATE SET tweeter.name = '" + follow.screen_name + "', tweeter.followers = " + str(follow.followers_count) + ", tweeter.description = '" + follow.description + "' RETURN tweeter.name")
            create_rel_tweeter2follow = graph.run("MATCH (n),(m) WHERE n.id = " + str(tweeter[0]['id']) + " AND m.id = " + follow.id_str + " MERGE (n)-[:FOLLOWS]->(m)")
        except:
            pass

# depending on the number of followers, you may run into an exceeded rate limit
