from collections import Counter
from datetime import timedelta, date

import sentiment_analysis as sa

import matplotlib.pyplot as plt


def get_date_boundaries(pos, neu, neg):
    total = pos
    total.extend(neu)
    total.extend(neg)
    return min(total), max(total)


def daterange(start_date, end_date):
    date_list = []
    for n in range(int((end_date - start_date).days+1)):
        date_list.append(start_date + timedelta(n))

    return dict.fromkeys(date_list, 0)


def plot(ratings, timestamps, total=None, page=""):
    date_positive = []
    date_neutral = []
    date_negative = []

    for i in range(0, len(ratings)):

        date = timestamps[i].replace(hour=0, minute=0, second=0, microsecond=0)

        if ratings[i] == sa.RATING_POSITIVE:
            date_positive.append(date)
        elif ratings[i] == sa.RATING_NEGATIVE:
            date_negative.append(date)
        else:
            date_neutral.append(date)

    occ_positive = Counter(date_positive)
    occ_neutral = Counter(date_neutral)
    occ_negative = Counter(date_negative)



    min_date, max_date = get_date_boundaries(date_positive, date_negative, date_neutral)

    date_range = daterange(min_date, max_date)

    occ_positive.update(date_range)
    occ_negative.update(date_range)
    occ_neutral.update(date_range)

    occ_total = None
    if total:
        total = [t['timestamp'].replace(hour=0, minute=0, second=0, microsecond=0) for t in total]
        occ_total = Counter(total)
        occ_total.update(date_range)

    draw_plot(occ_positive, occ_negative, occ_neutral, occ_total, page)


def draw_plot(pos, neg, neut, total, page):

    fig = plt.figure(figsize=(15, 4))
    ax = fig.add_subplot(1, 1, 1)

    if total:
        ax.bar(total.keys(), total.values(), color='0.9', edgecolor='none', width=1, label="total posts")

    ax.bar(neg.keys(), neg.values(), color='r', edgecolor="none", width=1, label="negative")
    ax.bar(neut.keys(), neut.values(), color='0.7', edgecolor="none", bottom=neg.values(), width=1, label="neutral")
    ax.bar(pos.keys(), pos.values(), color='g', edgecolor="none", bottom=[neg.values()[i] + neut.values()[i] for i in range(len(neut.values()))], width=1, label="positive")
    ax.xaxis_date()

    fig.subplots_adjust(right=0.85, left=0.1)

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    fig.autofmt_xdate()

    plt.ylabel("Number of Posts")
    plt.title("{0}".format(page))
    # plt.savefig('results/plot/plot_sentiment_'+page+'.png')
    plt.show()