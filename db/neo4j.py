from neo4j import GraphDatabase

class Neo4jDatabase:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return result

# Example usage
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "strongpassword123"

neo4j_db = Neo4jDatabase(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

# Example query
# result = neo4j_db.run_query("MATCH (n) RETURN n LIMIT 5")
# for record in result:
#     print(record)

__all__ = ['Neo4jDatabase', 'neo4j_db']
