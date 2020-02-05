from functools import *
from cnn import *
from twitter import *
from flask import Flask, render_template
from news import SimpleArticle as Article
from sentiment import *

cnn = Cnn(Article)
twitter = Twitter(Article)
application = Flask(__name__)

@application.route('/')
def main(*args):
    news = twitter.get_tweets()
    news.extend(cnn.get_news())
    news = list(map(classify_sentiment, news)) # Add sentiment analysis
    news.sort(key = lambda article: article.time_published, reverse = True)

    return render_template('index.html', news = news)

