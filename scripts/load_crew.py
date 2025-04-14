from datetime import timedelta
import time
import csv
from neo4j import GraphDatabase
from pathlib import Path
from utils import config
from utils.cypher_loader import load_cypher_query

BATCH_SIZE = 5000
DATA_FILE = Path("data/title.crew.tsv")
CREW_QUERY = load_cypher_query("insert_crew.cypher")

def transform_row(row):
    def clean(val, conv):
        return None if val == "\\N" else conv(val)

    return {
        "titleId": int(row["tconst"][2:]) if row["tconst"].startswith("tt") else None,
        "directors": clean(row["directors"], lambda val: [int(d[2:]) for d in val.split(",") if d]),
        "writers": clean(row["writers"], lambda val: [int(w[2:]) for w in val.split(",") if w])
    }

def load_crew(tx, batch):
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
                print(f"Error in row {processed_rows+1}: " + str(row))
                raise

            batch.append(processedRow)
            processed_rows += 1

            if len(batch) >= BATCH_SIZE:
                session.execute_write(load_crew, batch)
                batch = []
                percentage = (processed_rows / total_rows) * 100
                print(f"\rProcessing {DATA_FILE.name} {int(percentage)}%", end="")

        if batch:
            session.execute_write(load_crew, batch)

        elapsed = time.time() - startTime
        print(f"\rProcessing {DATA_FILE.name} Done in {timedelta(seconds=round(elapsed))}")

    driver.close()

if __name__ == "__main__":
    run()