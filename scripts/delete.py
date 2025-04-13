from neo4j import GraphDatabase
from utils import config

BATCH_SIZE = 10000

def drop_constraints(tx):
    tx.run("DROP CONSTRAINT title_id_unique IF EXISTS")
    tx.run("DROP CONSTRAINT name_id_unique IF EXISTS")
    tx.run("DROP CONSTRAINT genre_type_unique IF EXISTS")


def delete_relationships_batch(tx, batch_size):
    result = tx.run(
        """
        MATCH ()-[r]->() LIMIT $batch_size DELETE r
        RETURN count(r) AS deleted
        """,
        batch_size=batch_size
    )
    return result.single()["deleted"]


def delete_nodes_batch(tx, batch_size):
    result = tx.run(
        """
        MATCH (n) LIMIT $batch_size DELETE n
        RETURN count(n) AS deleted
        """,
        batch_size=batch_size
    )
    return result.single()["deleted"]


def run():
    driver = GraphDatabase.driver(
        config.NEO4J_URI,
        auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
    )

    with driver.session() as session:
        print("Dropping constraints...", end="")
        session.execute_write(drop_constraints)
        print("\rDropping constraints: Done!")
        
        
        deleted_total = 0
        print("Deleting relationships... 0", end="")
        
        while True:
            deleted_count = session.execute_write(delete_relationships_batch, BATCH_SIZE)
            deleted_total += deleted_count
            print(f"\rDeleting relationships.. {deleted_total}", end="")
            if deleted_count == 0:
                break
        print(f"\rDeleting relationships.. {deleted_total} Done!")
        
        
        deleted_total = 0
        print("Deleting nodes... 0", end="")
        
        while True:
            deleted_count = session.execute_write(delete_nodes_batch, BATCH_SIZE)
            deleted_total += deleted_count
            print(f"\rDeleting nodes.. {deleted_total}", end="")
            if deleted_count == 0:
                break
        print(f"\rDeleting nodes.. {deleted_total} Done!")


    driver.close()

if __name__ == "__main__":
    run()
