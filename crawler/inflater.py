from crawler.naked_api import App
from crawler.twitter_config import BEARER_TOKEN
import requests

def get_users_from_db_and_reqeust(app):
    users = app.get_empty_users()
    if len(users) < 20:
        return None
    users_list = ",".join(users)
    endpoint = 'https://api.twitter.com/2/users'
    headers = {'Authorization': "Bearer " + BEARER_TOKEN}
    params = {
        'ids': users_list,
        'user.fields': 'created_at,description,entities,public_metrics,username,verified,location',
    }
    res = requests.get(endpoint, params=params, headers=headers)
    res = res.json()
    return res

def user_process(app, response):
    for user_obj in response['data']:
        app.create_user(user_obj)
        app.create_descr_entities(user_obj)
        print(user_obj)

def get_empty_tweets_from_db_and_request(app):
    tweets = app.get_empty_tweets()
    if len(tweets) < 4:
        return None
    tweets_list = ",".join(tweets)
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
    res = res.json()
    return res

def tweet_process(app, response):
    for user_obj in response['includes']['users']:
        app.create_user(user_obj)
        app.create_descr_entities(user_obj)
    for tweet in response['data']:
        app.process_tweet(tweet, response['includes']['tweets'])

if __name__ == "__main__":
    # See https://neo4j.com/developer/aura-connect-driver/ for Aura specific connection URL.
    scheme = "bolt"  # Connecting to Aura, use the "neo4j+s" URI scheme
    host_name = "52.165.132.195"
    # neo4jqmap
    port = 7687
    url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
    user = "neo4j"
    password = "neo4jqmap"
    app = App(url, user, password)
    response = get_users_from_db_and_reqeust(app)
    if response is not None:
        user_process(app, response)
    response = get_empty_tweets_from_db_and_request(app)
    if response is not None:
        tweet_process(app, response)
    app.close()
