from opensearchpy import OpenSearch

from opensearch_rag.config.setting import HOST, PORT

client = OpenSearch(
    hosts=[{
        "host": OPENSEARCH_HOST,
        "port": OPENSEARCH_PORT
    }],
    http_compress=True
)

INDEX_NAME = "vector_store"

index_body = {
    "settings": {
        "index": {
            "knn": True
        }
    },
    "mappings": {
        "properties": {
            "vector": {
                "type": "knn_vector",
                "dimension": 384
            },
            "metadata": {
                "type": "object",
                "enabled": True
            }
        }
    }
}