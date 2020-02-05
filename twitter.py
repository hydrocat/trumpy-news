import tweepy
import os

class Twitter(object):
    """Retrieves tweets from a twitter account"""
    page = 0
    accountId = 25073877 # @realDonaldTrump account id
    
    def __init__(self, article_class, twitter_account = 25073877): # @realDonaldTrump account id
        """
        article_class: A class reference that implements SimpleArticle 'interface'
        twitter_account: int -- Number that represents a twitter id (defaults to @realDonaldTrump)
        """
        self.accountId = twitter_account
        self.Article = article_class

    def authenticate(self):
        self.auth = tweepy.OAuthHandler(os.environ["CKEY"], os.environ["CSECRET"])
        self.auth.set_access_token(os.environ["ATOKEN"], os.environ["TSECRET"])
        self.api = tweepy.API(self.auth)

    def get_tweets(self):
        """
        () -> List[article_class]
        Retrieves more or less (depends on twitter) 35 full-length tweets every call
        """

        # Sometimes, twitter answers with only one tweet, requiring authentication all over again
        self.authenticate()
        public_tweets = self.api.user_timeline(self.accountId, count=40, include_rts=False, page=self.page)
        self.page += 1

        full_tweets = []
        for tweet in public_tweets:
            if tweet.truncated == True:
                tweet = self.api.get_status(tweet.id, tweet_mode="extended")
                tweet.text = tweet.full_text
            full_tweets.append(self.Article(title = tweet.text,
                                            link = f"https://twitter.com/user/status/{tweet.id}",
                                            time_published = tweet.created_at,                                            
                                            original_data = tweet,
                                            source = "Twitter"))
        return full_tweets

if __name__ == "__main__":
    from news import SimpleArticle as Article
    twitter = Twitter(article_class = Article)
    for tweet in twitter.get_tweets():
        print(f'> {tweet.title}')
