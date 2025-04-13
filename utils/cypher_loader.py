
from utils.config import CYPHER_PATH

def load_cypher_query(cypher_filename):
    try:
        with open(CYPHER_PATH + cypher_filename, 'r') as file:
            cypher_query = file.read()
        return cypher_query
    except Exception as e:
        print(f"Error loading Cypher file {cypher_filename}: {e}")
        return None
