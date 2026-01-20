
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()
HOST = os.getenv("OPENSEARCH_HOST")
PORT = os.getenv("OPENSEARCH_PORT")
INDEX_NAME = os.getenv("INDEX_NAME")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    temperature = 0
)

client = OpenSearch(hosts=[{"host": HOST, "port": PORT}])
model = SentenceTransformer("all-MiniLM-L6-v2")


prompt = ChatPromptTemplate.from_template("""
You are an AI assistant.
Use ONLY the context below to answer the question.

Context:
{context}

Question:
{question}
""")

def retrieve(query, k=3):
    vector = model.encode(query).tolist()
    body = {
        "size": k,
        "query": {"knn": {"embedding": {"vector": vector, "k": k}}}
    }
    res = client.search(index=INDEX_NAME, body=body)
    return [hit["_source"]["metadata"]["text"] for hit in res["hits"]["hits"]]


def rag_answer(question: str):
    docs = retrieve(question)

    context = "\n\n".join(docs)

    messages = prompt.format_messages(
        context=context,
        question=question
    )

    response = llm.invoke(messages)
    return response.content



if __name__ == "__main__":
    answer = rag_answer("What is Hamza's experience in Generative AI?")
    print(answer)