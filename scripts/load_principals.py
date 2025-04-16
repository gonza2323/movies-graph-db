import csv
import json
import os
import time
from datetime import timedelta
from pathlib import Path

from neo4j import GraphDatabase

from utils import config
from utils import query
from utils.cypher_loader import load_cypher_query

BATCH_SIZE = 5000
DATA_FILE = Path("data/title.principals.tsv")
CREW_QUERY = load_cypher_query("insert_principals.cypher")


def transform_row(row):
    def clean(val, conv):
        return None if val == "\\N" else conv(val)

    return {
        "titleId": int(row["tconst"][2:]),
        "nameId": int(row["nconst"][2:]),
        "category": clean(row["category"], str),
        "job": clean(row["job"], str),
        "character": clean(row["characters"], lambda cs: "|".join(json.loads(cs)))
    }


def load_principals(tx, batch):
    tx.run(CREW_QUERY, rows=batch)


def run():
    startTime = time.time()
    query.run("create_name_id_constraint.cypher")

    print(f"Processing {DATA_FILE.name} 0%", end="")
    driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))
    total_rows = sum(1 for line in open(DATA_FILE, encoding="utf-8")) - 1
    batch = []

    with driver.session() as session, open(DATA_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        processed_rows = 0

        for row in reader:
            try:
                processedRow = transform_row(row)
            except Exception as e:
                print(f"Error in row {processed_rows + 1}: " + str(row))
                raise

            batch.append(processedRow)
            processed_rows += 1

            if len(batch) >= BATCH_SIZE:
                session.execute_write(load_principals, batch)
                batch = []
                percentage = (processed_rows / total_rows) * 100
                print(f"\rProcessing {DATA_FILE.name} {int(percentage)}%", end="")

        if batch:
            session.execute_write(load_principals, batch)

        elapsed = time.time() - startTime
        print(f"\rProcessing {DATA_FILE.name} Done in {timedelta(seconds=round(elapsed))}")

    driver.close()


if __name__ == "__main__":
    filename = os.path.basename(__file__)
    print(f"PRECAUCIÓN: Ejecutar {filename} cuando ya se han cargado roles creará datos duplicados.")
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
