from fastapi import APIRouter
from injection import injest_pdf
from retrieval import rag_answer


router = APIRouter(
    prefix = "/user",
    tags = "User"
)

@router.post("/ingest")
def ingest():
    pass