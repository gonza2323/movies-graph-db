import csv
import time
from datetime import timedelta
from pathlib import Path

from neo4j import GraphDatabase

from utils import config
from utils.cypher_loader import load_cypher_query

BATCH_SIZE = 5000
DATA_FILE = Path("data/title.ratings.tsv")
CREW_QUERY = load_cypher_query("insert_ratings.cypher")


def transform_row(row):
    def clean(val, conv):
        return None if val == "\\N" else conv(val)

    C = 5  # Constant for the average rating
    m = 5000  # Minimum votes threshold

    r = clean(row["averageRating"], float)
    v = clean(row["numVotes"], int)

    return {
        "id": int(row["tconst"][2:]) if row["tconst"].startswith("tt") else None,
        "averageRating": r,
        "numVotes": v,
        "weightedRating": (v / (v + m)) * r + (m / (v + m)) * C if r is not None and v is not None else 0
    }


def load_ratings(tx, batch):
    tx.run(CREW_QUERY, rows=batch)


def run():
    startTime = time.time()
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
                session.execute_write(load_ratings, batch)
                batch = []
                percentage = (processed_rows / total_rows) * 100
                print(f"\rProcessing {DATA_FILE.name} {int(percentage)}%", end="")

        if batch:
            session.execute_write(load_ratings, batch)

        elapsed = time.time() - startTime
        print(f"\rProcessing {DATA_FILE.name} Done in {timedelta(seconds=round(elapsed))}")

    driver.close()


if __name__ == "__main__":
    run()
