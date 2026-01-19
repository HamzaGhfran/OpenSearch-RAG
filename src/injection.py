
import sys
import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.setting import HOST, PORT




client = OpenSearch(
    hosts=[{
        "host": HOST,
        "port": PORT
    }],
    http_compress=True
)

INDEX_NAME = "vector_store"

def create_index():

    if client.indices.exists(index=INDEX_NAME):
        return
    body = {
        "settings": {"index": {"knn": True}},
        "mappings": {
            "properties": {
                "embedding": {"type": "knn_vector", "dimension": 384},
                "metadata": {"type": "object", "enabled": True}
            }
        }
    }
    client.indices.create(index=INDEX_NAME, body=body)


def read_pdf(file_path):

    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def split_text(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200
    )
    return splitter.split_text(text)

def ingest_pdf(file_path):

    create_index()
    text = read_pdf(file_path)
    chunks = split_text(text)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        doc = {
            "embedding": embedding,
            "metadata": {"text": chunk, "source": os.path.basename(file_path)}
        }
        client.index(index=INDEX_NAME, id=f"{os.path.basename(file_path)}_{i}", body=doc)

    print(f"Ingested {len(chunks)} chunks from {file_path}.")


if __name__ == "__main__":
    file_path = "/mnt/c/Users/Muhammad Hamza/Desktop/opensearch_rag/Hamza'sAI__Resume.pdf" 
    ingest_pdf(file_path)
