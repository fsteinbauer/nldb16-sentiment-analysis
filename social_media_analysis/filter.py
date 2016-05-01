# encoding=utf8

def keywords(posts, words):
    filtered_posts = []

    # F**k Python for no proper unicode handling.....
    import locale
    import sys
    locale.setlocale(locale.LC_ALL, 'deu_deu')
    reload(sys)
    sys.setdefaultencoding('utf-8')

    for post in posts:
        for keyword in words:

            if keyword.lower() in post['message'].encode('latin-1').lower():
                filtered_posts.append(post)
                break

    return filtered_posts
