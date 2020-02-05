from functools import *
from cnn import *
from twitter import *
from flask import Flask, render_template
from news import SimpleArticle as Article
cnn = Cnn(Article)
twitter = Twitter(Article)

app = Flask(__name__)

@app.route('/')
def main():
    news = twitter.get_tweets()
    news.extend(cnn.get_news())
    news.sort(key = lambda article: article.time_published, reverse = True)

    return render_template('index.html', news = news)

# for article in news:
#     print(article)
# for feed in raw_feeds:
#     for article in feed.entries:
#         news.extend(feed.entries)

# for article in news[:5]:
#     print(f"{article.title}\n{article.title_detail}\n{article.summary}\n{article.summary_detail}\n")

