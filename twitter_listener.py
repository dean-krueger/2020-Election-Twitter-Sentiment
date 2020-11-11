#!/usr/bin/env python3

import tweepy
import json

#All the keys and tokens from twitter (mine have been removed). To generate your own, see the twitter API documentation.

consumer_key = "your consumer key from twitter"
consumer_secret = "your consumer secret from twitter"
access_token = "your access token from twitter"
access_token_secret = "your access_token_secret from twitter"


#A simple recorder class which is inherited by the listener to allow writing to a json file as tweets are streamed.
class recorder:

	def __init__(self, filename):
		self.f = filename


	#record all the tweets
	def record(self, data):
		
		#grab the data from the stream and parse it with json
		data = json.loads(data)

		#if the tweet has coordinates, record its content, the time it was posted, and the coordinates.
		try:
			if(data["coordinates"] != None):
				print(data["text"])
				tweet = {}
				tweet["text"] = data["text"]
				tweet["time"] = data["created_at"]
				tweet["Longitude"] = data["coordinates"]["coordinates"][0]
				tweet["Latitude"] = data["coordinates"]["coordinates"][1]
				

				#keep appending the file being written to. This is not the best way to do this, but it works for now
				with open(self.f, "a") as file:
					file.write(str(json.dumps(tweet)))
					file.write("\n")
				
		except:
			pass


#The standard listener recomended by tweepy tutorials with the addition of the recorder so the stream can be recorded.
class Listener(tweepy.StreamListener):

	def __init__(self, recorder):
		self.r = recorder

	def on_data(self, data):
		self.r.record(data)
		return True



#main section
if __name__ == "__main__":


	#The three regions of tweets we're interested in (States in the USA)
	Alaska = [-180, 51.2, -130, 71.6]
	Hawaii = [ -160, 18.9, -154, 22.2]
	US = [-124.3, 25.8, -66.9, 49.4]


	#instaniate everything
	tweetRecorder = recorder("tweets_7.json")
	l = Listener(tweetRecorder)


	#Authenticate using provided credentials for access to twitter data
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)


	#Starts the stream and gives it the appropriate location filter
	stream = tweepy.Stream(auth = auth, listener=l)
	stream.filter(locations=US+Alaska+Hawaii)
	

