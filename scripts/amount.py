from neo4j import GraphDatabase

from utils import config


def get_counts(tx):
    labels_query = tx.run("CALL db.labels()")
    labels = [record["label"] for record in labels_query]

    results = {}

    results["relationships"] = tx.run("MATCH ()-[r]->() RETURN count(r) AS count").single()["count"]
    results["nodes"] = tx.run("MATCH (x) RETURN count(x) AS count").single()["count"]

    for label in labels:
        results[label] = tx.run(f"MATCH (x:{label}) RETURN count(x) AS count").single()["count"]
    
    return results



def run():
    driver = GraphDatabase.driver(
        config.NEO4J_URI,
        auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
    )

    with driver.session() as session:
        counts = session.execute_write(get_counts)
    
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    max_key_length = max(len(key) for key, count in sorted_counts)

    print(f"{'Key'.ljust(max_key_length)}  {'Count'}")
    print("-" * (max_key_length + 12))

    for key, count in sorted_counts:
        capitalized_key = key[0].upper() + key[1:]
        print(f"{capitalized_key.ljust(max_key_length)}  {count}")



if __name__ == "__main__":
    run()
