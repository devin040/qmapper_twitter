import requests
import json
from neo4j import GraphDatabase
from crawler.twitter_config import USER, PASSWORD
import spacy

url = 'bolt://52.165.132.195:7687'
db = GraphDatabase.driver(url, auth=(USER, PASSWORD))


def save_q_drop(driver, qdrop):
    with driver.session() as session:
        result = session.write_transaction(_save_q_drop, qdrop)
        for record in result:
            print("Created Q Drop: {record}".format(record=record))


def _save_q_drop(tx, qdrop):
    query = (
        "MERGE(q:QPOST {created_at: $timestamp}) "
        "ON CREATE SET q.text=$text "
        "RETURN q.created_at as time"
    )
    result = tx.run(query, text=qdrop['text'], timestamp=qdrop['timestamp'])
    return [record["time"] for record in result]


def get_qdrops_and_save():
    response = requests.get("https://qanon.pub/data/json/posts.json")

    response_json = response.json()

    for drop in response_json:
        save_q_drop(db, drop)



get_qdrops_and_save()

# qdrops = db.session().run("Match (q:QPOST) return q.text as text LIMIT 20")
# nlp = spacy.load('en_core_web_sm')
# for drop in qdrops:
#     doc = nlp(drop['text'])
#     print(drop['text'])
#     print("****************************************")
#     for token in doc:
#         if token.pos_ == "PROPN":
#             print(token.lemma_)
#     print('----------')
#     for ent in doc.ents:
#         print(ent.text, ent.label_)
#     print('*********************************************')