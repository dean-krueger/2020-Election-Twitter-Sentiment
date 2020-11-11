///////////////////////////////////////////////////////////////////
/                                                                 /
/              2020 Election Twitter Sentiment                    /
/                        Dean Krueger                             /
/                                                                 /
///////////////////////////////////////////////////////////////////


Brief Description:
------------------
This project is based off of an intro to computer science project I
did while in school at the University of Colorado, and its purpose
is to use the information available through the twitter API to learn
about how people in a certain region feel about a set of given topics.
I started this project near the end of the 2020 Presidential election,
and so I chose the two candidates (Donald Trump and Joe Biden) as the
subjects for my analysis, and set to work with the goal of being able
to learn about how people were feeling about them leading in to the
election. I planned on doing a very simple analysis, explained later
in the README, to assign scores to each tweet made about either
candidate, and then to figure out which state the tweet came from.
Once tweets were sorted by state, the scores would be summed up and
a total score assigned to each state for which there was data. Finally
a map would be generated in the style of a political map, like you might
see on election night, showing the overall political slant of each state
based on the sum of all scores from within that state. 


Analysis:
---------
The analysis performed was a very basic form of sentiment analysis, and
involved comparing tweets made about each candidate to a list of words
to which "sentiment scores" were assigned. The file I used for scoring is
the same one from my computer science project when I was in school, and so
its origin is sadly lost to me. However, many similar lists of words and
sentiment scores are available, such as the Sentiment Lexicon from the
university of Pittsburgh. Tweets from the stream were searched for a list 
of keywords designed to pick out tweets made about each candidate (one list
for each candidate), and then each word in each relevant tweet was scored
by comparing it to the sentiment list. This was done by indexing a dictionary
(because of the speed of that operation), and if a word was not found, the
score for the tweet overall was unchanged. Finally, because the map displays
red colors on the negative scale, and blue on the positive, tweets for which
the subject was Donald Trump had the sign of their score flipped so that
scores favoring the then president displayed red on the map, and those 
favoring Joe Biden displayed blue. A consequence of this is that tweets
made about the president which had a negative sentiment added to Biden's
score, and vice versa (which is what we wanted).

Files:
------
twitter_listener.py: uses tweepy and the twitter API to listen in on the
twitter stream and write tweets from the United States to a file. The
contents of the tweet, time the tweet was made, and lat/long geo data
are all recorded in the json file format. Filtering of tweets by keyword
cannot be done by the listener, sadly, since if a geo filter, and a keyword
filter are applied they are treated as being filtered by either or, and not
both.

tweet_scorer.py: reads in json files filled with tweets as well as a file
containing sentiment scores. Filters the tweets by keyword, then assigns
a score to each tweet. Finally creates and writes to a file, storing the 
score of each tweet, the time it was tweeted, and the lat/long.

map_maker.ipynb: jupyter notebook file which sorts the tweets by state,
then makes the map using folium.

sentiments.csv: the file which contains all the sentiment scores I used in
this project.

NOTE: Because of doxing worries, it felt irresponsible to upload the files
containing the tweets and their locations. This also includes the scored
tweets file, however I have uploaded the maps which resulted from them,
and may in the future modify the code to mask the location of the tweets 
and just display from which state they were created. The tweets I gathered
were made between Oct 27, 2020 and Nov 6, 2020.

Future Plans:
-------------
Modify code to mask the location of the tweets earlier (in the scored tweets
file) so that can be posted.

Find a more up to date sentiment dictionary with more certain origins

Modify scoring algorithm to reflect more complex and modern sentiment analysis
techniques to improve accuracy.

Add features to the folium map to display each state's score, as well as the
margin by which the winner of the state won in the election. 

