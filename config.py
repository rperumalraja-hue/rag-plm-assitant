import os

# Configuration
DB_PATH = "./chroma_db"
DOCS_PATH = "./data_source/documents"
DATA_PATH = "./data_source/structured_data"
MODEL_NAME = "llama3.2"
EMBEDDING_MODEL = "nomic-embed-text"

# Ensure directories exist
os.makedirs(DB_PATH, exist_ok=True)
os.makedirs(DOCS_PATH, exist_ok=True)
os.makedirs(DATA_PATH, exist_ok=True)