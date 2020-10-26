import json
import time
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import crawler.utilities
from crawler.twitter_config import USER, PASSWORD

url = 'bolt://52.165.132.195:7687'

driver = GraphDatabase.driver(url, auth=(USER, PASSWORD))

db = driver.session()

results = db.run("MATCH (a:Author)-[tw:Tweets]->(t:Tweet)-[c:CONTEXT]->(e:Entity) "
             "RETURN a.username as name,a.id as a_id, t.text as tweet, t.id as t_id,collect(e) as context  "
             "LIMIT 100")
#newresults = db.run("match (n:Entity)<-[r]-(t:Tweet) return n.data as ent, t.id as t_id, count(r) as Indegree order by Indegree desc Limit 100")
print(results)
nodes = []
rels = []
for record in results:
    author = {"name": record['name'], "id":record['a_id'], "label": "author"}
    try:
        nodes.index(author)
    except ValueError:
        nodes.append(author)
    auth_index = nodes.index(author)
    tweet = {"id": record['t_id'], "text": record['tweet'], "label":"tweet"}
    nodes.append(tweet)
    tweet_index = nodes.index(tweet)
    rels.append({"source": auth_index, "target": tweet_index})
    for entity in record['context']:
        if 'data' not in entity:
            continue
        entity_node = {"name": entity['data'], "id": entity['id'], "label": "context_entity"}
        try:
            target = nodes.index(entity_node)
        except ValueError:
            nodes.append(entity_node)
            target = nodes.index(entity_node)
        target = nodes.index(entity_node)
        rels.append({"source": tweet_index, "target": target})


print(nodes)
print(rels)
json_dict = {"nodes": nodes, "links": rels}
with open('d3test3.json', "w+") as outfile:
    json.dump(json_dict, outfile)