
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch
import os
from dotenv import load_dotenv


load_dotenv()
HOST = os.getenv("OPENSEARCH_HOST")
PORT = int(os.getenv("OPENSEARCH_PORT"))
INDEX_NAME = os.getenv("INDEX_NAME")

client = OpenSearch(hosts=[{"host": HOST, "port": PORT}])
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, k=3):
    vector = model.encode(query).tolist()
    body = {
        "size": k,
        "query": {"knn": {"embedding": {"vector": vector, "k": k}}}
    }
    res = client.search(index=INDEX_NAME, body=body)
    return [hit["_source"]["metadata"]["text"] for hit in res["hits"]["hits"]]



results = retrieve("")
for r in results:
    print(r)