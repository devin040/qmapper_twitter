import requests
import json
import time
import tweepy
import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from baseURL import get_base_domain
import utilities
from twitter_config import BEARER_TOKEN


headers = {'Authorization': "Bearer " + BEARER_TOKEN}

endpoint = 'https://api.twitter.com/2/tweets/search/recent'

params = {'query': '#QANON',
          'max_results': '10',
          'expansions': 'author_id,referenced_tweets.id,in_reply_to_user_id,geo.place_id',
          'place.fields': 'contained_within,country,full_name,geo,id,name,place_type',
          'tweet.fields': 'source,author_id,created_at,entities,in_reply_to_user_id,public_metrics,referenced_tweets,lang,geo,context_annotations',
          'user.fields': 'created_at,description,entities,public_metrics,username,verified,location',
          }

res = requests.get(endpoint, params=params, headers=headers)

print(res.json())
response = res.json()
print("hi")


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_friendship(self, person1_name, person2_name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_friendship, person1_name, person2_name)
            for record in result:
                print("Created friendship between: {p1}, {p2}".format(
                    p1=record['p1'], p2=record['p2']))

    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name):

        # To learn more about the Cypher syntax,
        # see https://neo4j.com/docs/cypher-manual/current/

        # The Reference Card is also a good resource for keywords,
        # see https://neo4j.com/docs/cypher-refcard/current/

        query = (
            "MERGE (p1:Person { name: $person1_name }) "
            "MERGE (p2:Person { name: $person2_name }) "
            "MERGE (p1)-[:Follows]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": record["p1"]["name"], "p2": record["p2"]["name"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def process_tweet(self, tweet, ref_tweets=None):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_and_return_tweet, tweet)
            for record in result:
                print("Created tweet with id {id}".format(
                    id=record['t1']))
        if 'referenced_tweets' in tweet:
            for ref_tweet in tweet['referenced_tweets']:
                if utilities.find_ref_tweet_by_id(ref_tweets, ref_tweet['id']) is not None:
                    self.process_tweet(utilities.find_ref_tweet_by_id(ref_tweets, ref_tweet['id']), ref_tweets)
                rel = "RETWEET"
                if ref_tweet['type'] == 'quoted':
                    rel = "QUOTES"
                if ref_tweet['type'] == "replied_to":
                    rel = "REPLY_TO"
                with self.driver.session() as session:
                    session.write_transaction(self._connect_ref_tweets, tweet['id'], ref_tweet['id'], rel)
        if 'entities' in tweet:
            if 'hashtags' in tweet['entities']:
                for item in tweet['entities']['hashtags']:
                    with self.driver.session() as session:
                        session.write_transaction(self._create_tweet_entity_and_connect, item['tag'], tweet['id'], 'HASHTAGS')
            if 'mentions' in tweet['entities']:
                for item in tweet['entities']['mentions']:
                    with self.driver.session() as session:
                        session.write_transaction(self._create_tweet_entity_and_connect, item['username'], tweet['id'], "MENTIONS")
            if 'urls' in tweet['entities']:
                for item in tweet['entities']['urls']:
                    with self.driver.session() as session:
                        session.write_transaction(self._create_tweet_entity_and_connect, get_base_domain(item['expanded_url']), tweet['id'], "LINKS")
            if 'annotations' in tweet['entities']:
                for item in tweet['entities']['annotations']:
                    with self.driver.session() as session:
                        session.write_transaction(self._create_tweet_entity_and_connect, item['normalized_text'], tweet['id'], 'ANNOTATES', annotate_type=item['type'])

        if 'context_annotations' in tweet:
            for ca in tweet['context_annotations']:
                with self.driver.session() as session:
                    session.write_transaction(self._create_and_connect_tweet_context_annotation, tweet['id'], ca)

    ###########################
    # Tweet Processing !!
    #############################
    @staticmethod
    def _create_and_return_tweet(tx, tweet):
        id = tweet['id']
        created_at = tweet['created_at']
        text = tweet['text']
        lang = tweet['lang']
        author_id = tweet['author_id']
        retweet_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        quote_count = tweet['public_metrics']['quote_count']

        query = ("MERGE (a1:Person:Author {id: $author_id}) "
                 "MERGE (t1:Tweet {id: $id}) "
                 "ON CREATE SET t1.created_at = $created_at, t1.text=$text, t1.lang=$lang, "
                 "                              t1.retweet_count=$retweet_count, t1.reply_count=$reply_count, "
                 "                               t1.like_count=$like_count, t1.quote_count=$quote_count "
                 "ON MATCH SET t1.retweet_count=$retweet_count, t1.reply_count=$reply_count, "
                 "             t1.like_count=$like_count, t1.quote_count=$quote_count "
                 "MERGE (a1)-[:Tweets]->(t1) "   
                 "RETURN a1, t1")
        result = tx.run(query, id=id, created_at=created_at, lang=lang, text=text, author_id=author_id,
                        retweet_count=retweet_count, reply_count=reply_count, like_count=like_count, quote_count=quote_count)
        try:
            return [{"a1": record["a1"]["id"], "t1": record["t1"]["id"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    @staticmethod
    def _connect_ref_tweets(tx, tweet1_id, tweet2_id, rel):
        rel = rel
        query = "MERGE (t1:Tweet {id: $t1_id}) "
        query += "MERGE (t2:Tweet {id: $t2_id}) "
        query += f"MERGE (t1)-[:{rel}]->(t2) RETURN t1, t2"
        result = tx.run(query, t1_id=tweet1_id, t2_id=tweet2_id)
        try:
            return [{"t1": record["t1"]["id"], "t2": record["t2"]["id"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))

    @staticmethod
    def _create_tweet_entity_and_connect(tx, entity, tweet_id, rel_type, annotate_type=None):
        query = "MERGE (t1:Tweet {id: $tweet_id}) "
        if rel_type == 'HASHTAGS':
            query += "MERGE (e1:Entity:Hashtag {data: $entity}) "
        elif rel_type == "MENTIONS":
            query += "MERGE (e1:Person {username: $entity}) "
        elif rel_type == "LINKS":
            query += "MERGE (e1:Entity:URL {data: $entity}) "
        elif rel_type == "ANNOTATES":
            query += f"MERGE (e1:Entity:{annotate_type.replace(' ', '_')} {{data: $entity}}) "
        query += f"MERGE (t1)-[:{rel_type}]->(e1) RETURN t1, e1"
        result = tx.run(query, tweet_id=tweet_id, entity=entity)
        try:
            return [{"t1": record["t1"]["id"], "e1": record["e1"]["data"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))

    @staticmethod
    def _create_and_connect_tweet_context_annotation(tx, tweet_id, annotationObject):
        domain=annotationObject['domain']
        entity=annotationObject['entity']
        query = f"MERGE (e1:Entity:{domain['name'].replace(' ', '_')} {{id:$e_id}}) "
        query += "ON CREATE SET e1.data=$e_name "
        query += "MERGE (d1:Domain {id:$d_id}) ON CREATE SET d1.name=$d_name, d1.description=$d_descr "
        query += "MERGE (t1:Tweet {id:$tweet_id}) "
        query += "MERGE (t1)-[:CONTEXT]->(e1) "
        query += "MERGE (t1)-[:CONTEXT]->(d1) "
        query += "RETURN t1, e1, d1"
        result = tx.run(query, tweet_id=tweet_id, e_name=entity['name'], e_id=entity['id'], d_id=domain['id'],
                        d_name=domain['name'], d_descr=domain['description'])
        try:
            return [{"e1": record["e1"]["name"], "d1": record["d1"]["name"], "t1": record["t1"]["id"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))




    @staticmethod
    def _create_and_return_user(tx, twitter_user):

        # To learn more about the Cypher syntax,
        # see https://neo4j.com/docs/cypher-manual/current/

        # The Reference Card is also a good resource for keywords,
        # see https://neo4j.com/docs/cypher-refcard/current/
        id = twitter_user['id']
        created_account = twitter_user['created_at']
        verified = str(twitter_user['verified'])
        username = twitter_user['username']
        follower_count = twitter_user['public_metrics']['followers_count']
        following_count = twitter_user['public_metrics']['following_count']
        tweet_count = twitter_user['public_metrics']['tweet_count']
        name = twitter_user['name']
        description = twitter_user['description']

        query = (
            "MERGE (p1:Person:Author { id: $id }) "
            "ON CREATE SET p1.name=$name, p1.created_account=$created_account, p1.verified=$verified,"
            "                             p1.username=$username, p1.follower_count=$follower_count, "
            "                             p1.following_count=$following_count, p1.tweet_count=$tweet_count,"
            "                               p1.description=$description "
            "RETURN p1"
        )
        result = tx.run(query, name=name, id=id, created_account=created_account, verified=verified, username=username,
                        follower_count=follower_count, following_count=following_count, tweet_count=tweet_count,
                        description=description)
        try:
            return [{"user": record['p1']['username']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    @staticmethod
    def _create_and_return_descr_hashtag(tx, entity, user_id):

        # To learn more about the Cypher syntax,
        # see https://neo4j.com/docs/cypher-manual/current/

        # The Reference Card is also a good resource for keywords,
        # see https://neo4j.com/docs/cypher-refcard/current/

        query = (
            "MERGE (p1:Person { id: $id }) "
            "MERGE (e1:Entity:Hashtag {data: $entity})"
            "MERGE (p1)-[:Describes]->(e1)"
            "RETURN e1"
        )
        result = tx.run(query, id=user_id, entity=entity)
        try:
            return [{"entity": record['e1']['data']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    @staticmethod
    def _create_and_return_descr_url(tx, entity, user_id):

        # To learn more about the Cypher syntax,
        # see https://neo4j.com/docs/cypher-manual/current/

        # The Reference Card is also a good resource for keywords,
        # see https://neo4j.com/docs/cypher-refcard/current/

        query = (
            "MERGE (p1:Person { id: $id }) "
            "MERGE (e1:Entity:URL {data: $entity})"
            "MERGE (p1)-[:Describes]->(e1)"
            "RETURN e1"
        )
        result = tx.run(query, id=user_id, entity=entity)
        try:
            return [{"entity": record['e1']['data']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    @staticmethod
    def _create_and_return_descr_mention(tx, entity, user_id):

        # To learn more about the Cypher syntax,
        # see https://neo4j.com/docs/cypher-manual/current/

        # The Reference Card is also a good resource for keywords,
        # see https://neo4j.com/docs/cypher-refcard/current/

        query = (
            "MERGE (p1:Person { id: $id }) "
            "MERGE (e1:Entity:Mention {data: $entity})"
            "MERGE (p1)-[:Describes]->(e1)"
            "RETURN e1"
        )
        result = tx.run(query, id=user_id, entity=entity)
        try:
            return [{"entity": record['e1']['data']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    @staticmethod
    def _create_and_return_descr_location(tx, entity, user_id):

        # To learn more about the Cypher syntax,
        # see https://neo4j.com/docs/cypher-manual/current/

        # The Reference Card is also a good resource for keywords,
        # see https://neo4j.com/docs/cypher-refcard/current/

        query = (
            "MERGE (p1:Person { id: $id }) "
            "MERGE (e1:Entity:Location {data: $entity})"
            "MERGE (p1)-[:Describes]->(e1)"
            "RETURN e1"
        )
        result = tx.run(query, id=user_id, entity=entity)
        try:
            return [{"entity": record['e1']['data']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_user(self, twitter_user):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_user, twitter_user)
            for record in result:
                print("Created user: {p1}".format(
                    p1=record['user']))

    def create_descr_entities(self, twitter_user):
        if 'entities' in twitter_user and 'description' in twitter_user['entities']:
            if 'hashtags' in twitter_user['entities']['description']:
                for tag in twitter_user['entities']['description']['hashtags']:
                    with self.driver.session() as session:
                        result = session.write_transaction(self._create_and_return_descr_hashtag, tag['tag'], twitter_user['id'])
                        print(result)
            if 'mentions' in twitter_user['entities']['description']:
                for mention in twitter_user['entities']['description']['mentions']:
                    with self.driver.session() as session:
                        result = session.write_transaction(self._create_and_return_descr_mention, mention['username'], twitter_user['id'])
                        print(result)
        if 'entities' in twitter_user and 'url' in twitter_user['entities']:
            for url in twitter_user['entities']['url']['urls']:
                baseurl = get_base_domain(url['expanded_url'])
                with self.driver.session() as session:
                    result = session.write_transaction(self._create_and_return_descr_url, baseurl, twitter_user['id'])
                    print(result)
        if 'location' in twitter_user:
            with self.driver.session() as session:
                result = session.write_transaction(self._create_and_return_descr_location, twitter_user['location'], twitter_user['id'])
                print(result)

    def find_person(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_person, person_name)
            for record in result:
                print("Found person: {record}".format(record=record))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [record["name"] for record in result]


if __name__ == "__main__":
    # See https://neo4j.com/developer/aura-connect-driver/ for Aura specific connection URL.
    scheme = "bolt"  # Connecting to Aura, use the "neo4j+s" URI scheme
    host_name = "13.59.234.229"
    # neo4jqmap
    port = 7687
    url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
    user = "neo4j"
    password = "neo4jqmap"
    app = App(url, user, password)
    for user in response['includes']['users']:
        app.create_user(user)
        app.create_descr_entities(user)
    for tweet in response['data']:
        app.process_tweet(tweet, response['includes']['tweets'])
    print("ey")
    app.close()
