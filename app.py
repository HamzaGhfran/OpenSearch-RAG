from fastapi import APIRouter
from opensearch_rag.src.api import router

api_router = APIRouter()

api_router.include_router(router)


