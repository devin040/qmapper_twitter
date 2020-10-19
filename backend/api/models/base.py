from neo4j import GraphDatabase

class Database:
    def __init__(self):
        self.app = None
        self.driver = None
    
    def init_app(self, app, uri, user, password):
        self.app = app
        self._uri = uri
        self._user = user
        self._password = password
        self.connect()

    def connect(self):
        self.db_driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
        return self.db_driver

    def get_db(self):
        if not self.db_driver:
            return self.connect()
        
        return self.db_driver

    def close(self):
        self.db_driver.close()


db = Database()
