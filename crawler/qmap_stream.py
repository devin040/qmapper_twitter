import json
import requests
from twitter_config import BEARER_TOKEN, USER, PASSWORD
from naked_api import App
import inflater as inflater
import sys
sys.path.append("D:\cs598kcc\qmapper_twitter")
#url = "https://api.twitter.com/2/tweets/search/stream?tweet.fields=source,author_id,created_at"

db_uri = "bolt://localhost:7687"


#print(response.text.encode('utf8'))

params = {
          'expansions': 'author_id,referenced_tweets.id,in_reply_to_user_id,geo.place_id',
          'place.fields': 'contained_within,country,full_name,geo,id,name,place_type',
          'tweet.fields': 'source,author_id,created_at,entities,in_reply_to_user_id,public_metrics,referenced_tweets,lang,geo,context_annotations',
          'user.fields': 'created_at,description,entities,public_metrics,username,verified,location',
          }


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(headers, bearer_token, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(headers, delete, bearer_token):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "#DarkToLight OR #TheGreatAwakening OR #QAnon OR #Q OR #WWG1WGA OR #WWG1WGAWORLDWIDE OR #SaveTheChildren", "tag": "QANON Standard"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(headers, set, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", headers=headers, params=params, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    app = App(db_uri, USER, PASSWORD)
    stream_count = 0
    for response_line in response.iter_lines():
        if response_line:
            stream_count += 1
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))
            for user in json_response['includes']['users']:
                try:
                    app.create_user(user)
                    app.create_descr_entities(user)
                except:
                    print(f"Error while making user {user}")
            ref_tweets = None
            if 'tweets' in json_response['includes']:
                ref_tweets = json_response['includes']['tweets']
            try:
                app.process_tweet(json_response['data'], ref_tweets)
            except:
                print(f"Error in processing Tweet")



def main():
    bearer_token = BEARER_TOKEN
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, None, bearer_token)
    get_stream(headers, None, bearer_token)


if __name__ == "__main__":
    main()
