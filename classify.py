import sys
import argparse
import facebook
import time
from time import mktime
from datetime import datetime

from social_media_analysis.post_import import import_facebook
from social_media_analysis.sentiment_analysis import classify_posts
from social_media_analysis.plot import plot
from social_media_analysis.filter import keywords

def valid_date(s):
    try:
        return datetime.fromtimestamp(mktime(time.strptime(s, "%Y-%m-%d"))).date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Import and analyze posts from facebook')

    parser.add_argument('page',
                       help='Facebook page to import')
    parser.add_argument('--access_token', required=True,
                       help='Facebook access token. To gain an access_token please check the documentation')
    parser.add_argument('--date_start', type=valid_date,
                        help='The starting date to import posts - format YYYY-MM-DD')
    parser.add_argument('--date_end', type=valid_date,
                        help='The ending date to import posts - format YYYY-MM-DD')
    parser.add_argument('--keywords', nargs="+",
                        help="List of keywords separated by space. Only posts containing these keywords will be classifies and plotted")

    args = parser.parse_args()

    # Load the posts into a dict
    try:
        posts = import_facebook(args.access_token, args.page, args.date_start, args.date_end)
    except facebook.GraphAPIError:
        print "Error: Something went wrong while fetching the data from Facebook, \n \
make sure the access_token is valid and the page exists."
        sys.exit(-5)

    total = None
    if args.keywords:
        total = posts
        posts = keywords(posts, args.keywords)

    data = [d['message'] for d in posts]
    timestamps = [d['timestamp'] for d in posts]


    # Predict the posts
    prediction = classify_posts(data, timestamps)

    # plot the results
    plot(prediction, timestamps, total, args.page)



