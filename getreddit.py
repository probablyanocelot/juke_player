import requests
import json

pushshift_api_url = 'https://api.pushshift.io/reddit/search/'

# returns JSON


def get_data(sub_or_comment, subreddit, size):
    res = requests.get(pushshift_api_url +
                       f'{sub_or_comment}/?subreddit={subreddit}&size={size}')
    return res.json()['data']


def post_data(subreddit, size):
    return get_data('submission', subreddit, size)


def comment_data(subreddit, size):
    return get_data('comment', subreddit, size)


def filter_data(data, criteria=None):
    mydict = dict()
    counter = 0
    for item in data:
        if criteria in item['url']:
            if not 'shorts' in item['url'] and not 'playlist' in item['url']:
                mydict[counter] = {
                    'title': item['title'],
                    'url': item['url'],
                }
                counter += 1
    return json.dumps(mydict, indent=4)


def get_yt_subs(subreddit):
    posts = post_data(subreddit, 50)
    yt_posts = filter_data(posts, 'youtu')
    return yt_posts
