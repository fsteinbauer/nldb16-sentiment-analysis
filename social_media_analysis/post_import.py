# -*- coding: utf-8 -*-

import facebook
import requests
import sys
import string
import re
import datetime as dt
from dateutil.relativedelta import relativedelta
from dateutil import parser


def store_post(post, profile_id, date_start, date_end):

    # Filter out posts, created by the page and user stories
    if profile_id != post['from']['id'] and 'message' in post:

        timestamp = parser.parse(post['created_time'])

        # Check if post is between date start and end
        if timestamp.date() > date_start:
            return None

        if timestamp.date() < date_end:
            raise ValueError

        message = filter(lambda x: x in string.printable + 'äöüÄÖÜß', post['message'])
        message = message.replace('\n', ' ').strip('\r').strip('\n')
        message = re.sub(r"http\S+", "", message)

        row = {
            'timestamp': timestamp,
            'message': message
        }

        return row


def import_facebook(access_token, page, date_start=None, date_end=None):
    """

    @param access_token:
    @param page:
    @param date_start:
    @param date_end:
    @return:
    """

    # Get begining and end date
    if not date_start:
        date_start = dt.date.today()

    if not date_end:
        date_end = dt.date.today()-relativedelta(months=+12)

    # F**k Python for no proper unicode handling.....
    import locale
    locale.setlocale(locale.LC_ALL, 'deu_deu')
    reload(sys)
    sys.setdefaultencoding('utf8')

    # args = {
    #     'since': date_end.strftime("%Y-%m-%d"),
    #     'until': date_start.strftime("%Y-%m-%d")
    # }

    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object(page)
    posts = graph.get_connections(profile['id'], 'feed')
    posts_list = []

    while True:
        try:
            # Perform some action on each post in the collection we receive from
            # Facebook.
            for post in posts['data']:
                post = store_post(post, profile['id'], date_start, date_end)

                if post:
                    posts_list.append(post)

            print "Written Posts: ", len(posts_list)

            # Attempt to make a request to the next page of data, if it exists.
            posts = requests.get(posts['paging']['next']).json()

        except ValueError:
            break

        except KeyError:
            # When there are no more pages (['paging']['next']), break from the
            # loop and end the script.
            break


    return posts_list
