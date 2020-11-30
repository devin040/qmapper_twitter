from naked_api import App
from twitter_config import BEARER_TOKEN
import requests
import time


def get_users_from_db_and_request(app):
    users = app.get_empty_users()
    if len(users) < 16:
        return None
    users_list = ",".join(users)
    endpoint = 'https://api.twitter.com/2/users'
    headers = {'Authorization': "Bearer " + BEARER_TOKEN}
    params = {
        'ids': users_list,
        'user.fields': 'created_at,description,entities,public_metrics,username,verified,location',
    }
    res = requests.get(endpoint, params=params, headers=headers)
    while res.status_code != 200:
        print("Too many requests .. sleeping")
        time.sleep(60 * 5)
        res = requests.get(endpoint, params=params, headers=headers)
    res = res.json()
    return res


def user_process(app, response):
    for user_obj in response['data']:
        app.create_user(user_obj)
        app.create_descr_entities(user_obj)
        print(user_obj)


def get_mentioned_users_from_db(app):
    users = app.get_mentioned_only_users()
    if len(users) < 20:
        return None
    users_list = ",".join(users)
    endpoint = 'https://api.twitter.com/2/users/by'
    headers = {'Authorization': "Bearer " + BEARER_TOKEN}
    params = {
        'usernames': users_list,
        'user.fields': 'created_at,description,entities,public_metrics,username,verified,location',
    }
    res = requests.get(endpoint, params=params, headers=headers)
    while res.status_code != 200:
        print("Too many requests .. sleeping")
        time.sleep(60 * 3)
        res = requests.get(endpoint, params=params, headers=headers)
    res = res.json()
    return res

def get_empty_tweets_from_db_and_request(app):
    tweets = app.get_empty_tweets()
    if len(tweets) < 20:
        time.sleep(60)
        return None
    tweets_list = ",".join(tweets)
    print(tweets)
    endpoint = 'https://api.twitter.com/2/tweets'
    headers = {'Authorization': "Bearer " + BEARER_TOKEN}
    params = {
        'ids': tweets_list,
        'expansions': 'author_id,referenced_tweets.id,in_reply_to_user_id,geo.place_id',
        'place.fields': 'contained_within,country,full_name,geo,id,name,place_type',
        'tweet.fields': 'source,author_id,created_at,entities,in_reply_to_user_id,public_metrics,referenced_tweets,lang,geo,context_annotations',
        'user.fields': 'created_at,description,entities,public_metrics,username,verified,location',
    }
    res = requests.get(endpoint, params=params, headers=headers)
    while res.status_code != 200:
        print("Too many requests .. sleeping")
        time.sleep(60 * 5)
        res = requests.get(endpoint, params=params, headers=headers)
    res = res.json()
    return res


def tweet_process(app, response):
    try:
        if 'errors' in response:
            for error in response['errors']:
                app.setHiddenTweetById(error.get('value', None), error.get('title', 'Not Found Error'))
        for user_obj in response['includes']['users']:
            app.create_user(user_obj)
            app.create_descr_entities(user_obj)
        for tweet in response['data']:
            ref_tweets = None
            if "tweets" in response['includes']:
                ref_tweets = response['includes']['tweets']
            app.process_tweet(tweet, ref_tweets)
    except KeyError:
        print("****************ERRROR*******************")
        print(response)




if __name__ == "__main__":
    # See https://neo4j.com/developer/aura-connect-driver/ for Aura specific connection URL.
    scheme = "bolt"  # Connecting to Aura, use the "neo4j+s" URI scheme
    host_name = "localhost"
    # neo4jqmap
    port = 7687
    url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
    user = "neo4j"
    password = "neo4jqmap"
    count = 0
    while True:
        count += 1
        app = App(url, user, password)
        if count == 3:
            count = 0
            app.merge_mentions_and_authors()
            app.make_interacts_rels()
            app.make_weighted_interacts_rels()
        u_response = get_users_from_db_and_request(app)
        if u_response is not None:
            user_process(app, u_response)
        t_response = get_empty_tweets_from_db_and_request(app)
        if t_response is not None:
            tweet_process(app, t_response)
        m_response = get_mentioned_users_from_db(app)
        if m_response is not None:
            user_process(app, m_response)
        if t_response is None and u_response is None and m_response is None:
            time.sleep(60)
        app.close()
