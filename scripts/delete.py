import os
from neo4j import GraphDatabase
from utils import config
from utils.cypher_loader import load_cypher_query
from utils.config import NEO4J_DB

BATCH_SIZE = 10000

QUERIES=load_cypher_query("recreate_database.cypher") \
    .replace("DB_NAME", NEO4J_DB) \
    .strip().splitlines()

def recreate_database(tx):
    for query in QUERIES:
        tx.run(query)

def run():
    driver = GraphDatabase.driver(
        config.NEO4J_URI,
        database="system",
        auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
    )

    with driver.session() as session:
        print(f"Recreating database '{NEO4J_DB}'...", end="")
        session.execute_write(recreate_database)
        print(f"\rRecreating database '{NEO4J_DB}': Done!")
    
    driver.close()

if __name__ == "__main__":
    filename = os.path.basename(__file__)
    print(f"PRECAUCIÓN: Ejecutar {filename} borrará todas las restricciones, relaciones y nodos en la base de datos.")
    while True:
        user_input = input("Quiere proceder? [y/n]: ").strip().lower()
        if user_input in ("y", "yes"):
            run()
            break
        elif user_input in ("n", "no"):
            print("Cancelado.")
            break
        else:
            print("Input inválido. Ingrese y(es) / n(o).")