from neo4j import GraphDatabase
from utils import config

LABELS=["Obra", "Genero"]

def get_counts(tx):
    relationships = tx.run("MATCH ()-[r]->() RETURN count(r) AS count")
    nodes = tx.run("MATCH (x) RETURN count(x) AS count")
    titles = tx.run("MATCH (x:Obra) RETURN count(x) AS count")
    genres = tx.run("MATCH (x:Genero) RETURN count(x) AS count")

    return relationships.single()["count"], nodes.single()["count"], titles.single()["count"], genres.single()["count"]


def run():
    driver = GraphDatabase.driver(
        config.NEO4J_URI,
        auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
    )

    with driver.session() as session:
        counts = session.execute_write(get_counts)
        print(f"""Relationships: {counts[0]},
Nodes: {counts[1]},
Titles: {counts[2]},
Genres: {counts[3]}""")

    driver.close()

if __name__ == "__main__":
    run()
