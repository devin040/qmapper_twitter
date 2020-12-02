from neo4j import GraphDatabase
from api import config
import os


class DegreeCentrality:

    def __init__(self):
        env = os.environ.get("FLASK_ENV", "dev")
        self.uri = config[env].DATABASE_URI
        self.user = config[env].DATABASE_USER
        self.password = config[env].DATABASE_PASS
        self.db_driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def get_indegree(self):
        ret = []
        with self.db_driver.session() as session:
            results = session.run(
                "MATCH  (u:User) RETURN size(collect( u.username)) AS num ,size((u)<-[:INTERACTS_W]-()) AS indegree ORDER BY indegree desc").data()
            nums = [result['num'] for result in results]
            total = sum(nums)
            indegrees = [result['indegree'] for result in results]
            for x in range(len(indegrees)):
                up_to = len(indegrees)-x
                sanity = nums[:up_to]
                su = sum(nums[x:])
                pct = su / total
                ret.append({"degree": indegrees[x], "pct": pct})
            return ret[::-1]

    def get_outdegree(self):
        ret = []
        with self.db_driver.session() as session:
            results = session.run(
                "MATCH  (u:User) RETURN size(collect( u.username)) AS num ,size((u)-[:INTERACTS_W]->()) AS outdegree ORDER BY outdegree desc").data()
            nums = [result['num'] for result in results]
            total = sum(nums)
            indegrees = [result['outdegree'] for result in results]
            for x in range(len(indegrees)):
                up_to = len(indegrees)-x
                sanity = nums[:up_to]
                su = sum(nums[x:])
                pct = su / total
                ret.append({"degree": indegrees[x], "pct": pct})
            return ret[::-1]

    def close(self):
        self.db_driver.close()

