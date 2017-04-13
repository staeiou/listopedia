import random
import twitter_login
import tweepy
import markovify
import wordfilter
import pickle

# Tact function modified from function in cyberprefixer 
# (c) Molly White, 2013-2016, released MIT License
# https://github.com/molly/CyberPrefixer/blob/master/offensive.py

import offensive


with open ("titles_over_60_chars_cleaned.txt", encoding="utf-8") as f:
    deltext = f.read()

deltext = deltext.replace(".", " ")
deltext = deltext.encode('ascii', 'ignore').decode('ascii')

with open("past_titles.txt", encoding="utf-8") as f2:
    past_titles = f2.read()

past_titles_l = past_titles.split("\n")

# In[3]:

try:
    with open("deletion_model.pkl", "rb") as pickle_in:
        deletion_model = pickle.load(pickle_in)

except Exception as e:
    deletion_model = markovify.NewlineText(deltext)

    with open('deletion_model.pkl', 'wb') as pickle_out:
        pickle.dump(deletion_model, pickle_out)

# In[4]:

tweet = None
tweets = []
for i in range(1000):
    title = deletion_model.make_sentence_with_start("List of", min_chars=80, max_chars=110)
    if title is not None and not wordfilter.blacklisted(title) and offensive.tact(title) and title not in past_titles_l and len(title) < 110 and len(title) > 80:
        tweets.append(title)

tweets = sorted(tweets, key=len, reverse=True)
rand_num = random.randrange(0,10)


# In[5]:

if tweets[rand_num] is not None:
    print(tweets[rand_num])


CONSUMER_KEY = twitter_login.CONSUMER_KEY
CONSUMER_SECRET = twitter_login.CONSUMER_SECRET
ACCESS_TOKEN = twitter_login.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = twitter_login.ACCESS_TOKEN_SECRET

# Authenticate

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

api.update_status(tweets[rand_num])

with open("past_titles.txt", "a") as f:
    f.write(tweets[rand_num])
