import sys
import time
from datetime import timedelta

from neo4j import GraphDatabase

from utils import config
from utils.cypher_loader import load_cypher_query


def _run_query(tx, QUERY):
    tx.run(QUERY)


def run(cypher_file_name):
    startTime = time.time()
    print(f"Processing query {cypher_file_name}...", end="")

    driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))
    queries = load_cypher_query(cypher_file_name).split(';')

    with driver.session() as session:
        for query in queries:
            if query.strip():
                session.execute_write(_run_query, query + ';')

    elapsed = time.time() - startTime
    print(f"\rProcessing query {cypher_file_name} Done in {timedelta(seconds=round(elapsed))}")

    driver.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1]:
        cypher_file_name = sys.argv[1]
        run(cypher_file_name)
    else:
        print("Usage is utils.run_query <cypher_file_name>")
