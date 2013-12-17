from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import sys
import db
import json

ckey = 'g3xJmsw62CWj4XTZpopqg'
csecret = 'oMOIZUn6ZwqvqqavPMvV0nqbiigrOWwjo97IqJEHKqo'
atoken = '285503765-LHwtFvf5ZoevpA3bBHVEDP8EtotWgnHZTfffxVay'
asecret = '8mWIId8UHcvA1LGPT3A6lT4uewG6dlt3usy1ZVJ8U40Bu'

totalTweets = 1
con = db.dbconnect()

class listener(StreamListener):
	def on_data(self, data):
		data = json.loads(data)
		global totalTweets
		try:
			tweet = str(data['text'])
			user = str(data['user']['screen_name'])
			time = str(data['created_at'])
		except BaseException, e:
			tweet = ""
			user = ""
			time = ""

		if tweet != "" and user != "" and time != "":
			tweet = tweet.encode('base64','strict')
			con.query("INSERT INTO tweet (`by`, `tweet`, `time`) VALUES ('%s', '%s', '%s')" % (user, tweet, time))
			sys.stdout.write("\rTotal tweets: %i" % totalTweets)
			totalTweets += 1
			sys.stdout.flush()

	def on_error(self, status):
		print("\rERROR:::" + str(status))

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
inp = raw_input("Input a filter: ")
print("Listening on twitter stream for tweets containing: " + inp)
twitterStream.filter(track=[inp])