import collections
import sys
import csv
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem.snowball import SnowballStemmer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.externals import joblib

from tqdm import tqdm


RATING_NEGATIVE = 'negative'
RATING_POSITIVE = 'positive'
RATING_NEUTRAL = 'neutral'

RATING_SUBJECTIVE = 'subjective'
RATING_OBJECTIVE = 'objective'
BOUNDARY_NEGATIVE = -0.35
BOUNDARY_POSTITVE = 0.35

reload(sys)
sys.setdefaultencoding("utf-8")

stemmer = SnowballStemmer("german")
tokenizer = TreebankWordTokenizer()


def import_posts(filename):
    """
    This function reads a csv file into a list

    @param filename The file to be opened

    @return: A tuple
    """
    posts = []

    with open(filename, 'r') as csv_file:

        reader = csv.reader(csv_file, delimiter=",", quotechar='"')

        count = 1
        for row in reader:
            # skip missing data
            count += 1
            if row[0] and row[1] and row[2] and count < 100000:
                rating = extract_sentiment(float(row[0]), float(row[1]))

                posts.append((
                    rating,
                    row[2],
                    extract_subjectivity(rating)
                ))

    return posts


def extract_subjectivity(rating):
    """

    @param rating:
    @return:
    """
    if rating is RATING_NEUTRAL:
        return RATING_NEUTRAL
    else:
        return RATING_SUBJECTIVE


def tokenize(input_string):
    input_string = tokenizer.tokenize(input_string)
    input_string = [word.lower() for word in input_string]
    input_string = [word for word in input_string if word not in stopwords.words('german')]
    input_string = [stemmer.stem(word) for word in input_string]
    return input_string


def extract_sentiment(pos, neg):
    rating = (pos - neg) / 10

    if rating <= BOUNDARY_NEGATIVE:
        return RATING_NEGATIVE
    elif rating > BOUNDARY_POSTITVE:
        return RATING_POSITIVE

    return RATING_NEUTRAL


def filter_subjective(data, target):
    data_list = []
    target_list = []

    if len(data) != len(target):
        raise ValueError("Length of data and target do not match")

    for d, t in zip(data, target):
        if t != RATING_NEUTRAL:
            data_list.append(d)
            target_list.append(t)

    return data_list, target_list


def filter_objective(data, target):
    data_list = []
    target_list = []

    if len(data) != len(target):
        raise ValueError("Length of data and target do not match")

    for d, t in zip(data, target):
        if t == RATING_NEUTRAL:
            data_list.append(d)
            target_list.append(t)

    return data_list, target_list


def list_to_map(data, target):
    data = [hash(row) for row in data]
    sorted_list = sorted(zip(data, target), key=lambda tup: tup[0])

    if len(data) != len(set(data)):
        raise RuntimeError("List does not contain unique data ({0} vs. {1})".format(len(data), len(set(data))))

    return [x[1] for x in sorted_list]


def get_subjectivity_pipeline():
    return Pipeline([
        ('count_vectorizer', CountVectorizer(ngram_range=(1, 1), tokenizer=tokenize, binary='true')),
        ('tfidf_transformer', TfidfTransformer()),
        ('classifier', LinearSVC())
    ])


def get_polarity_pipeline():
    return Pipeline([
        ('count_vectorizer', CountVectorizer(ngram_range=(1, 2), tokenizer=tokenize, binary='true')),
        ('tfidf_transformer', TfidfTransformer()),
        ('classifier', LinearSVC())
    ])


def classify_posts(posts, timestamps):
    print "Loading Classifiers ..."
    classifiers = joblib.load('pickle/classifier.pkl')

    print "Predicting {0} posts ...".format(len(posts))
    ratings = []
    for post, timestamp in tqdm(zip(posts, timestamps)):
        rating = classifiers['subjectivity'].predict([post])

        if rating[0] == RATING_SUBJECTIVE:
            rating = classifiers['polarity'].predict([post])

        ratings.append(rating[0])

    return ratings