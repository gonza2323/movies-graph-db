import os
import csv
from neo4j import GraphDatabase
from pathlib import Path
from utils import config
from utils.cypher_loader import load_cypher_query
from utils import run_query

BATCH_SIZE = 5000
DATA_FILE = Path("data/title.principals.tsv")
CREW_QUERY = load_cypher_query("insert_principals.cypher")

def transform_row(row):
    def clean(val, conv):
        return None if val == "\\N" else conv(val)

    return {
        "titleId": int(row["tconst"][2:]) if row["tconst"].startswith("tt") else None,
        "nameId": int(row["nconst"][2:]) if row["nconst"].startswith("nm") else None,
        "category": clean(row["category"], str),
        "job": clean(row["job"], str),
        "characters": clean(row["characters"], lambda val: [c.strip() for c in val.split(",") if c.strip()])
    }

def load_principals(tx, batch):
    tx.run(CREW_QUERY, rows=batch)

def run():
    driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))
    total_rows = sum(1 for line in open(DATA_FILE, encoding="utf-8")) - 1
    batch = []

    with driver.session() as session, open(DATA_FILE, encoding="utf-8") as f:
        print(f"Processing {DATA_FILE.name} 0%", end="")
        reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        processed_rows = 0

        for row in reader:
            try:
                processedRow = transform_row(row)
            except Exception as e:
                print(f"Error in row {processed_rows+1}: " + str(row))
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

        print(f"\rProcessing {DATA_FILE.name} Done    ")

    driver.close()

if __name__ == "__main__":
    run()