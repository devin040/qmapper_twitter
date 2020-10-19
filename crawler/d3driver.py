import json
import time
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import utilities
from twitter_config import USER, PASSWORD

url = 'bolt://3.137.190.174:7687'

driver = GraphDatabase.driver(url, auth=(USER, PASSWORD))

db = driver.session()

results = db.run("MATCH (a:Author)-[tw:Tweets]->(t:Tweet)-[c:CONTEXT]->(e:Entity) "
             "RETURN a.username as name,a.id as a_id, t.text as tweet, t.id as t_id,collect(e) as context  "
             "LIMIT 100")
print(results)
nodes = []
rels = []
for record in results:
    author = {"name": record['name'], "id":record['a_id'], "label": "author"}
    try:
        nodes.index(author)
    except ValueError:
        nodes.append(author)
    nodes.append({"id": record['t_id'], "text": record['tweet'], "label":"tweet"})
    rels.append({"source": record['a_id'], "target": record['t_id']})
    for entity in record['context']:
        if 'data' not in entity:
            continue
        entity_node = {"name": entity['data'], "id": entity['id'], "label": "context_entity"}
        try:
            target = nodes.index(entity_node)
        except ValueError:
            nodes.append(entity_node)
            target = nodes.index(entity_node)
        rels.append({"source": record['t_id'], "target": entity_node['id']})

print(nodes)
print(rels)
json_dict = {"nodes": nodes, "links": rels}
with open('d3test.json', "w+") as outfile:
    json.dump(json_dict, outfile)