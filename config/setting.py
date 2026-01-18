import os
from dotenv import load_dotenv  

load_dotenv()

HOST = os.getenv("OPENSEARCH_HOST", "127.0.0.1")
PORT = os.getenv("OPENSEARCH_PORT", "9200")