
from utils.config import CYPHER_PATH
from os import path

def load_cypher_query(cypher_file_name):
    try:
        file_path=path.join(CYPHER_PATH, cypher_file_name)
        with open(file_path, 'r') as file:
            cypher_query = file.read()
        return cypher_query
    except Exception as e:
        print(f"Error loading Cypher file {cypher_file_name}: {e}")
        return None
