from functools import *
import feedparser
import datetime

class Cnn(object):
    """Retrieve news from CNN's RSS feed"""
    feed_list = [
        "http://rss.cnn.com/rss/edition_world.rss",
        "http://rss.cnn.com/rss/edition_us.rss",
        "http://rss.cnn.com/rss/money_news_international.rss"
    ]

    search_terms = ['Trump']

    def __init__(self, article_class, feeds = [], search_terms = []):
        """
        article_class: A class reference that implements SimpleArticle 'interface'
        feeds: List[str] -- Additional rss urls
        search_terms: List[str] -- Additional search terms
        """
        self.Article = article_class
        self.feed_list.extend(feeds)
        self.search_terms.extend( search_terms )

    def isTrump(self, article):
        """
        article: a Feed from feedparser.parse
        Compares wether an article mentions Trump
        """
        text = (article.title + article.summary).lower()
        return any([text.find(term.lower()) > -1 for term in self.search_terms])

    def get_news(self):
        """
        () -> List[article_class]
        """
        news = []
        for feed in [feedparser.parse(f) for f in self.feed_list]:
            trump_news = filter(self.isTrump, feed.entries)
            for article in trump_news:
                img_position = article.summary.find("<img")
                article.summary = article.summary[:img_position]
                simple_article = self.Article(
                    title = article.title,
                    summary = article.summary,
                    link = article.id,
                    source = 'CNN',
                    time_published = datetime.datetime(*article.published_parsed[:6])
                )
                news.append(simple_article)
        return news
        

if __name__ == '__main__':
    from news import SimpleArticle as Article
    cnn = Cnn(Article)
    for article in cnn.get_news():
        print(f"{article.title}\n{article.summary}\n")

