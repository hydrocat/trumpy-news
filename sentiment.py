from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk import download
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from news import SimpleArticle

# Resourcing a dataset
nltk.download('subjectivity', download_dir = "nltk")
nltk.download('punkt')
nltk.download('vader_lexicon')

## Generating dataset
instances = 100
subjective_sentences = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:instances]]
objective_sentences = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:instances]]

# Divied each dataset into 20% test, 80% train
train_subjective = subjective_sentences[:80]
test_subjective  = subjective_sentences[80:]

train_objective = objective_sentences[:80]
test_objective =  objective_sentences[80:]

training_docs = train_objective + train_subjective
testing_docs  = test_objective  + test_subjective

analyzer = SentimentAnalyzer()
negative_words = analyzer.all_words([mark_negation(doc) for doc in training_docs])

features = analyzer.unigram_word_feats(negative_words, min_freq=4)
analyzer.add_feat_extractor(extract_unigram_feats, unigrams=features)

training_set = analyzer.apply_features(training_docs)
test_set     = analyzer.apply_features(testing_docs)

## Training the classifier
trainer = NaiveBayesClassifier.train
classifier = analyzer.train(trainer, training_set)

for key,value in sorted(analyzer.evaluate(test_set).items()):
    print('{0}: {1}'.format(key, value))

print("NLP classifier ready")

def sentiment(text):
    """
    text: str
    return: 'positive'| 'negative' | 'neutral'
    classifies a text into 'positive', 'negative' or 'neutral'
    averages the classification of all internal sentences
    """
    lines_list = tokenize.sent_tokenize(text)
    sid = SentimentIntensityAnalyzer()

    compound = 0
    for sentence in lines_list:
        ss = sid.polarity_scores(sentence)
        compound += ss["compound"]
    compound /= len(lines_list)

    if compound > 0.5:
        return 'positive'
    elif compound < 0.5:
        return 'negative'
    else:
        return 'neutral'

def classify_sentiment(article):
    """
    use the trained model to classify an article as negative, positive or neutral
    article: SimpleArticle
    return: SimpleArticle
    """
    
    feeling = sentiment(f'{article.title} .{article.summary}. {article.content}' )
    article.sentiment = feeling
    return article
