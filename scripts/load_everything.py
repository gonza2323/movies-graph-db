import os
from datetime import timedelta
import time
from scripts import load_titles
from scripts import load_names
from scripts import load_crew
from scripts import load_principals
from scripts import load_episodes
from scripts import load_ratings
from utils import query

def run():
    startTime = time.time()
    print("Loading data into database")
    
    load_titles.run()
    query.run("delete_invalid_data.cypher")
    load_names.run()
    load_ratings.run()
    query.run("create_indexes.cypher")
    load_episodes.run()
    load_principals.run()
    load_crew.run()
    
    elapsed = time.time() - startTime
    print(f"Finished loading data in {timedelta(seconds=round(elapsed))}")
    

if __name__ == "__main__":
    filename = os.path.basename(__file__)
    print(f"PRECAUCIÓN: Ejecutar {filename} cuando ya se han cargado datos creará datos duplicados.")
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
