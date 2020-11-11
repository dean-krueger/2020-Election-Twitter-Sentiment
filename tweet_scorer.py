#!/usr/bin/env python3

import glob
import json


def hasKeywords(str, keys):
	"""
	Checks a string for certain keywords. Returns true if ANY are found

	Arguments:
	---------------
	str - The string to be checked
	keys - a list of keywords for which str will be searched


	Returns:
	---------------
	True - if ANY of the strings in keys are found within str
	False - if NONE of the strings in keys are found within str


	Example:
	---------------
	ex_string = "the quick brown fox jumped over the lazy dog"

	hasKeywords(ex_string, ["brown", "elephant"]) --> True
	hasKeywords(ex_string, ["BROWN", "elephant"]) --> False
	hasKeywords(ex_string, ["cat", "pear"] --> False
	"""
	contains_keys = False
	for key in keys:
		if(str.find(key) != -1):
			contains_keys = True

	return contains_keys

def getSentiments(file):
	"""
	Reads in a file of word sentiment scores and stores them in a dictionary
	
	Arguments:
	---------------
	file -  The filepath to a csv containing words and sentiments in [word, sentiment] format.
			Assumes that data will be a list of strings, and that the "\n" character is present.


	Returns:
	---------------
	sentiments - A dictionary where the words from file are keys, and the scores are values. 
				 NOTE: all word keys are stored in all caps ("hey" --> "HEY") to avoid mismatches
				 	   on capitalization 


	Example:
	---------------
	path = "example.csv"
	sentiments = getSentiments(path)

	print(sentiments["Hello"]) --> 0.5

	"""
	sentiments = {}
	sentiments_file = open(file, "r")

	for line in sentiments_file:
		s = line.split(",")
		sentiments[s[0].strip(".,:;'-!?").upper()] = float(s[1].strip("\n"))

	#make sure to close the file when done reading
	sentiments_file.close()


	return sentiments

def score(tweet, sentiments, sign=1):
	"""
	Takes a list of words, assigns a score to all words in the list which have sentiment scores,
	and applies an optional sign for comparison of two sides of a spectrum. For example, comparison

	Arguments:
	---------------
	tweet - A list of words to be scored (called tweet because this is usually a split tweet)
	sentiments - A dictionary keyed by word with sentiment scores as values (sentiments["hello"] --> 0.5)
	sign - optional value if intending to compare two things on a spectrum (Republican <--> Democratic)

	Returns:
	---------------
	score - A float containing the sum total of word sentiment scores for the list overall.


	Example:
	---------------
	tweet_1 = ["YOU", "ARE", "A", "BAD", "DOG"]
	tweet_2 = ["YOU", "ARE", "A", "BAD", "BAD",  "DOG"]
	tweet_3 = ["YOU", "ARE", "A", "GOOD", "DOG"]
	sentiments = getSentiments("example.csv")

	print(score(tweet_1, sentiments)) --> -0.5
	print(score(tweet_2, sentiments)) --> -1.0
	print(score(tweet_3, sentiments)) --> 0.4
	print(score(tweet_3, sentiments, sign=-1)) --> -0.4

	"""
	score = 0.0
	w = ""
	for word in tweet:
		try:
			score = score + sign*sentiments[word]
		except:
			score = score
	return score


#grab all the json files which store tweets. These are not all the same size, but that is fine
files = glob.glob("*.json")

#remove the file which is active currently while we continue to collect tweets
#files.remove("tweets_7.json")

#set up two lists of keywords. "Left" corresponds to keywords focused on the democratic party candidate, "Right" the republican
leftKeys = ["DEMOCRAT", "DNC", "BIDEN", "@JOEBIDEN", "KAMALA"]
rightKeys = ["REPUBLICAN","TRUMP", "@REALDONALDTRUMP", "POTUS", "PENCE", "RNC"]


#import the sentiment word scores
sentiments = getSentiments("sentiments.csv")

#make a csv file to save the scores, times, and locations of all tweets, then add the header
write_to = open("scored_tweets.csv", "x")
write_to.write("Score,Time,Latitude,Longitude\n")

#score all tweets file by file (each line in the files is a separate json formatted tweet gathered from twitter)
for file in files:
	f = open(file, "r")
	for line in f:
		data = json.loads(line)

		#store all the components of the json file in variables. Note that .upper() is used to match the format of sentiments
		text = data["text"].upper()
		time = data["time"]
		latitude = data["Latitude"]
		longitude = data["Longitude"]

		#check for left or right keywords and assign appropriate sign
		if(hasKeywords(text, rightKeys)):
			split_text = text.split(" ")
			s = score(split_text, sentiments, sign=-1)
			if(s!=0):
				write_to.write(str(s) + "," + str(time) + "," + str(latitude) + "," + str(longitude) + "\n")

		elif(hasKeywords(text, leftKeys)):
			split_text = text.split(" ")
			s = score(split_text, sentiments)
			if(s!=0):
				write_to.write(str(s) + "," + str(time) + "," + str(latitude) + "," + str(longitude) + "\n")


#close all our files
	f.close()
f.close()
