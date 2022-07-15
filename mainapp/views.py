from django.shortcuts import render
from django.http import *
from mainapp.forms import *
import tweepy
import re
from textblob import TextBlob

# Create your views here.
class TwitterSent():
    def cleaning(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    def get_sentiment(self, tweet):
        analysis = TextBlob(self.cleaning(tweet))
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1
    
    def get_tweets(self, q, c = 100):
        res = []
        try:
            token = "AAAAAAAAAAAAAAAAAAAAANcqZAEAAAAAGYEzPg7EIh0WdnoTaS8rXSIYNdY%3Do7xtVBFN3NHnngr8IGYTS7fge66OInPe5GKp7F1GGcxwDAJyga"
            client = tweepy.Client(bearer_token = token)
            print("Authenticated")
            tweets = client.search_recent_tweets(query = q, max_results = c)
            for tweet in tweets.data:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_sentiment(tweet.text)
                if parsed_tweet not in res:
                    res.append(parsed_tweet)
            return res
        except tweepy.errors.TweepyException as e:
            print("Error :" + str(e))

def show(request):
	context = {}
	form = QueryForm()
	context['form'] = form
	return render(request, 'index.html', context)

def prediction(request):
	context = {}
	pos = []
	neg = []
	pos_text = []
	neg_text = []
	if request.method == "POST":
		api = TwitterSent()
		que = request.POST['twitterquery']
		tweets = api.get_tweets(q = que, c = 100)
		for tweet in tweets:
			if tweet['sentiment'] == 1:
				pos.append(tweet)
			elif tweet['sentiment'] == -1:
				neg.append(tweet)

		perc1 = 100 * (len(pos) / len(tweets))
		perc2 = 100 * (len(neg) / len(tweets))
		perc3 = 100 - (perc1 + perc2)
		for tweet in pos[:5]:
			pos_text.append(tweet['text'])
		for tweet in neg[:5]:
			neg_text.append(tweet['text'])

		context['percentage_pos'] = perc1
		context['percentage_neg'] = perc2
		context['percentage_neut'] = perc3
		context['pos'] = pos_text
		context['neg'] = neg_text
		context['len_pos'] = len(pos_text)
		context['len_neg'] = len(neg_text)

		return render(request, 'pred.html', context)