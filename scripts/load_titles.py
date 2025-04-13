import csv
import os
from neo4j import GraphDatabase
from pathlib import Path
from utils import config
from utils.cypher_loader import load_cypher_query
from utils import run_query

BATCH_SIZE = 5000
DATA_FILE = Path("data/title.basics.tsv")
TITLES_QUERY = load_cypher_query("insert_titles.cypher")

def transform_row(row):
    def clean(val, conv):
        return None if val == "\\N" else conv(val)

    return {
        "id": int(row["tconst"][2:]) if row["tconst"].startswith("tt") else None,
        "titleType": clean(row["titleType"], str),
        "primaryTitle": clean(row["primaryTitle"], str),
        "originalTitle": clean(row["originalTitle"], str),
        "isAdult": clean(row["isAdult"], lambda x: bool(int(x))),
        "startYear": clean(row["startYear"], int),
        "endYear": clean(row["endYear"], int),
        "runtimeMinutes": clean(row["runtimeMinutes"], int),
        "genres": clean(row["genres"], lambda val: [g.strip() for g in val.split(",") if g.strip() and g != "\\N"])
    }

def load_titles(tx, titleTypeTag, batch):
    final_query = TITLES_QUERY.replace("TitleType", titleTypeTag, 1)
    tx.run(final_query, rows=batch)

def run():
    run_query.run("create_genre_type_constraint.cypher")

    driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))
    total_rows = sum(1 for line in open(DATA_FILE, encoding="utf-8")) - 1
    batchesPerType = {}

    with driver.session() as session, open(DATA_FILE, encoding="utf-8") as f:
        print(f"Processing {DATA_FILE.name} 0%", end="")
        reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        processed_rows = 0

        for row in reader:
            try:
                processedRow = transform_row(row)
                titleType=processedRow["titleType"]
            except Exception as e:
                print(f"Error in row {processed_rows+1}: " + str(row))
                raise
            
            if processedRow["id"] is None:
                continue

            if titleType not in batchesPerType:
                batchesPerType[titleType] = []
            
            batchesPerType[titleType].append(processedRow)

            processed_rows += 1

            if len(batchesPerType[titleType]) >= BATCH_SIZE:
                session.execute_write(load_titles, titleType, batchesPerType[titleType])
                batchesPerType[titleType] = []
                percentage = (processed_rows / total_rows) * 100
                print(f"\rProcessing {DATA_FILE.name} {int(percentage)}%", end="")
            

        for titleType, batch in batchesPerType.items():
            if batch:
                session.execute_write(load_titles, titleType, batch)

        print(f"\rProcessing {DATA_FILE.name} Done    ")

    driver.close()

if __name__ == "__main__":
    filename = os.path.basename(__file__)
    print(f"PRECAUCIÓN: Ejecutar {filename} cuando ya se han cargado los datos, creará datos duplicados.")
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
