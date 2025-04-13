import sys
from neo4j import GraphDatabase
from utils import config
from utils.cypher_loader import load_cypher_query


def run_query(tx, QUERY):
    tx.run(QUERY)

def run(cypher_file_name):
    driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))
    QUERY = load_cypher_query(cypher_file_name)

    with driver.session() as session:
        print(f"Processing query {cypher_file_name}...", end="")
        session.execute_write(run_query, QUERY)
        print(f"\rProcessing query {cypher_file_name} Done")

    driver.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1]:
        cypher_file_name=sys.argv[1]
        run(cypher_file_name)
    else:
        print("Usage is utils.run_query <cypher_file_name>")
