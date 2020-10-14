import requests
import json
import time
import tweepy
import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from baseURL import get_base_domain

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

    def process_tweet(self, tweet):
        return 0

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
        if 'entities' in twitter_user and 'description' in twitter_user['entities'] and 'hashtags' in twitter_user['entities']['description']:
            entities = [entity['tag'] for entity in twitter_user['entities']['description']['hashtags']]
        else:
            entities = []

        query = (
            "MERGE (p1:Person { id: $id }) "
            "ON CREATE SET p1.name=$name, p1.created_account=$created_account, p1.verified=$verified,"
            "                             p1.username=$username, p1.follower_count=$follower_count, "
            "                             p1.following_count=$following_count, p1.tweet_count=$tweet_count,"
            "                               p1.description=$description, p1.entities=$entities "
            "RETURN p1"
        )
        result = tx.run(query, name=name, id=id, created_account=created_account, verified=verified, username=username,
                        follower_count=follower_count, following_count=following_count, tweet_count=tweet_count,
                        description=description, entities=entities)
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
    host_name = "3.137.199.246"
    # neo4jqmap
    port = 7687
    url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
    user = "neo4j"
    password = "neo4jqmap"
    app = App(url, user, password)
    for user in response['includes']['users']:
        app.create_user(user)
        app.create_descr_entities(user)
    print("ey")
    app.close()
