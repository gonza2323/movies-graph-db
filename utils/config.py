import os

from dotenv import load_dotenv

load_dotenv()  # loads .env file into environment variables

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_DB = os.getenv("NEO4J_DB")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
CYPHER_PATH = "cypher/"
