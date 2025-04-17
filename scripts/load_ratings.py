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

VOTES_THRESHOLD = 2000
AVERAGE_RATING = None


def clean(val, conv):
    return None if val == "\\N" else conv(val)

def get_avg_rating_and_total_rows():
    total = 0
    totalVotes = 0
    totalRows = 0

    with open(DATA_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

        for row in reader:
            rating = clean(row["averageRating"], float)
            numVotes = clean(row["numVotes"], int)

            if rating is not None and numVotes is not None:
                total += rating * numVotes
                totalVotes += numVotes
            
            totalRows += 1
        
    return total / totalVotes, totalRows

def transform_row(row):
    C = AVERAGE_RATING  
    m = VOTES_THRESHOLD

    r = clean(row["averageRating"], float)
    v = clean(row["numVotes"], int)

    if r is not None and v is not None:
        w = (v / (v + m)) * r + (m / (v + m)) * C
        w = round(w, 1)
    else:
        w = None

    return {
        "id": int(row["tconst"][2:]) if row["tconst"].startswith("tt") else None,
        "averageRating": r,
        "numVotes": v,
        "weightedRating": w
    }


def load_ratings(tx, batch):
    tx.run(CREW_QUERY, rows=batch)


def run():
    startTime = time.time()
    print(f"Processing {DATA_FILE.name} 0%", end="")

    global AVERAGE_RATING
    AVERAGE_RATING, total_rows = get_avg_rating_and_total_rows()

    driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))
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


if __name__ == "__main__":
    run()
