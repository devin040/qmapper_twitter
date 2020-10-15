from neo4j import GraphDatabase

class Database:
    def __init__(self, uri, user, password):
        self.db_driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.db_driver.close()

