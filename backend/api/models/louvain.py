from neo4j import GraphDatabase
from api import config
import os


class Louvain:

    def __init__(self):
        env = os.environ.get("FLASK_ENV", "dev")
        self.uri = config[env].DATABASE_URI
        self.user = config[env].DATABASE_USER
        self.password = config[env].DATABASE_PASS
        self.db_driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def get_stats(self):
        with self.db_driver.session() as session:
            stats = session.run("""
                                CALL gds.louvain.stats({nodeProjection: "User", relationshipProjection:"INTERACTS_W", relationshipProperties:"num", relationshipWeightProperty:"num"})
                                Yield communityCount, communityDistribution
                                Return communityCount, communityDistribution
                                """)
            return stats.data()

    def get_full_communities(self):
        ret = []
        with self.db_driver.session() as session:
            session.run("""
                        CALL gds.louvain.write({nodeProjection: "User", relationshipProjection:"INTERACTS_W", relationshipProperties:"num", relationshipWeightProperty:"num", writeProperty:"communityNum"})
                        """)
            communities = session.run("Match (n:User) Return n.communityNum as comId, count(*) AS size order by size desc LIMIT 5").data()
            comSizes= [community['size'] for community in communities]
            communityIds = [community['comId'] for community in communities]
            for x in range(len(communityIds)):
                com = communityIds[x]
                results = session.run(f"Match (n:User)-[r:INTERACTS_W]->(n2:User) where n.communityNum={com} with count(r) as cnt, n2 RETURN n2.username as user order by cnt desc LIMIT 3")
                topUsers = [result['user'] for result in results]
                results = session.run(f"\
                                        MATCH (u:User)-[:Tweets]->(t:Tweet)-[r:CONTEXT]->(e:Entity)\
                                        WHERE u.communityNum = {com} \
                                        WITH u,t,r,e \
                                        ORDER BY t.id DESC \
                                        LIMIT 1000 \
                                        RETURN count(r) AS indegree, e.data AS topic \
                                        ORDER BY indegree DESC\
                                        LIMIT 3\
                                      ")
                topTopics = [result['topic'] for result in results]
                ret.append({"topUsers": topUsers, "size": comSizes[x], "topTopics": topTopics})
            return ret

    def connect(self):
        self.db_driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        return self.db_driver

    def get_db(self):
        if not self.db_driver:
            return self.connect()

        return self.db_driver

    def close(self):
        self.db_driver.close()