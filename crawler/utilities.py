import ciso8601
import time
def convertTimeString(timestr):
    ts = ciso8601.parse_datetime(timestr)
    return time.mktime(ts.timetuple())

def find_ref_tweet_by_id(tweets, id):
    for tweet in tweets:
        if tweet['id'] == id:
            return tweet
    else:
        return None

def find_author_by_id(users, id):
    for user in users:
        if user['id'] == id:
            return user
    return None


print(convertTimeString("2020-10-14T21:29:23.000Z"))

