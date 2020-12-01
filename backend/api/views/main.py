from flask import Blueprint, request
from api.core import create_response, serialize_list
from api.models import db
from api.models.louvain import Louvain
from api.models.degreedistro import DegreeCentrality

main = Blueprint("main", __name__)


# function that is called when you visit /
@main.route("/")
def index():
    # you are now in the current application context with the main.route decorator
    return create_response(message="test message", data={"testdata": 1})


@main.route("/data")
def data():
    offset = int(request.args.get('offset'))
    limit = int(request.args.get('limit'))
    if offset is None or limit is None:
        return create_response(status=400, message="Required parameters not present")
    
    query = """
        MATCH (n)-[r]->(m)
        RETURN n, r, m
        ORDER BY n.id, r.id, m.id
        SKIP {}
        LIMIT {}
    """.format(offset, limit)

    with db.get_db().session() as session:
        result = session.run(query)
        return create_response(data={"data": result.data()})


@main.route("/topusers")
def top_users():
    with db.get_db().session() as session:
        result = session.run("""
            MATCH (a:User) 
            WHERE (a)-[:Tweets]-() and a.username IS NOT NULL AND a.follower_count IS NOT NULL
            RETURN a.username as username, a.follower_count as follower_count
            ORDER BY a.follower_count DESC
        """)
        return create_response(data={"data": result.data()})


@main.route("/toptweetusers")
def top_tweet_users():
    with db.get_db().session() as session:
        result = session.run("""
            MATCH (a:User) 
            WHERE a.username IS NOT NULL AND a.tweet_count IS NOT NULL
            RETURN a.username as username, a.tweet_count as tweet_count
            ORDER BY a.tweet_count DESC
        """)
        return create_response(data={"data": result.data()})


@main.route("/simpletrending")
def simple_trending():
    with db.get_db().session() as session:
        result = session.run("""
            MATCH (t:Tweet)-[r:CONTEXT]->(e:Entity) 
            WITH t,r,e 
            ORDER BY t.id DESC 
            LIMIT 1000 
            RETURN count(r) AS indegree, e.data AS topic 
            ORDER BY indegree DESC
        """)
        return create_response(data={"data": result.data()})

@main.route("/betweeness")
def betweeness():
    with db.get_db().session() as session:
        result = session.run("""
            CALL gds.betweenness.stream({nodeProjection: "User", relationshipProjection:"INTERACTS"})
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).username AS name, score, gds.util.asNode(nodeId).follower_count as followers
            ORDER BY score DESC
            LIMIT 50
        """)
        return create_response(data={"data": result.data()})

@main.route("/page_rank")
def page_rank():
    with db.get_db().session() as session:
        result = session.run("""
            CALL gds.pageRank.stream({nodeProjection: "User", relationshipProjection:"INTERACTS_W"})
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).username AS name, score, gds.util.asNode(nodeId).follower_count as followers
            ORDER BY score DESC
            LIMIT 50
        """)
        return create_response(data={"data": result.data()})

@main.route("/page_rank_weighted")
def page_rank_weighted():
    with db.get_db().session() as session:
        result = session.run("""
            CALL gds.pageRank.stream({nodeProjection: "User", relationshipProjection:"INTERACTS_W", relationshipProperties:"num", relationshipWeightProperty:"num"})
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).username AS name, score, gds.util.asNode(nodeId).follower_count as followers
            ORDER BY score DESC
            LIMIT 50
        """)
        return create_response(data={"data": result.data()})

@main.route("/louvainstats")
def louvain_stats():
    louv = Louvain()
    response = louv.get_stats()
    louv.close()
    return create_response(data={"data": response})

@main.route("/louvaindetail")
def louvain_detail():
    louv = Louvain()
    response = louv.get_full_communities()
    louv.close()
    return create_response(data={"data": response})


@main.route("/indegree")
def indegree_ccdf():
    d = DegreeCentrality()
    response = d.get_indegree()
    d.close()
    return create_response(data={"data": response})

@main.route("/outdegree")
def outdegree_ccdf():
    d = DegreeCentrality()
    response = d.get_outdegree()
    d.close()
    return create_response(data={"data": response})

@main.route("/metrics")
def metrics():
    pass
