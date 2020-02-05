# Trumpy News
A simple flask app that combines Tump's tweets and related CNN articles.

## Configuring:
_This is assuming that you're using bash_

1. Make yourself a virtual environment:
```sh
python -m venv .venv
```
Enter it:
```sh
source .venv/bin/activate
```

### 2. Install pip requirements:
```sh
pip install -r requirements.txt
```

3. Add the environment variables:
There are 4 variables required to access twitter and one for flask:
    - CKEY
        Consumer Key
    - CSECRET
        Consumer Secret
    - ATOKEN
        Authentication Token
    - TSECRET
        Token Secret
    - FLASK\_APP
        Required by Flask
        
_You have to get them from https://developer.twitter.com/_
    
```sh
export -x FLASK_APP=main.py
export -x CKEY=XX
export -x CSECRET=XX
export -x ATOKEN=XX
export -x TSECRET=XX
```


3. That's it.

## Running it:

```sh
gunicorn wsgi
```

4. Runtime Configurations
Let's say you want to tune it a bit, there are a few things that come to mind:

    - cnn.py
  The constructor has the following signature:
  ```python
      def __init__(self, article_class, feeds = [], search_terms = []):
  ```
  `feeds` is a optional list of RSS urls that are added to the pre-select 3 cnn sources.
  
  `search_terms` is another optional argument, takes in strings that, if found in the title or summary, considers the article as related to Trump.
  
  - twitter.py

    ```python
        def __init__(self, article_class, twitter_account = 25073877):
    ```
    
    The optional argument **twitter_account** is the twitter id of the desired user whose tweets will be queried. Defaults to @realDonaldtrump.
