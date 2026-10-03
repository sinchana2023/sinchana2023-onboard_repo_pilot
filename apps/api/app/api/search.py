from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.search import SearchRequest, SearchResponse
from app.services.retrieval_service import RetrievalService


router = APIRouter(
    prefix="/api/v1/repositories",
    tags=["search"],
)


@router.post(
    "/{repository_id}/search",
    response_model=SearchResponse,
)
def search_repository(
    repository_id: int,
    request: SearchRequest,
    db: Session = Depends(get_db),
):
    retrieval_service = RetrievalService()

    results = retrieval_service.search(
        repository_id=repository_id,
        query=request.query,
        db=db,
        top_k=request.top_k,
    )

    return {
        "results": results,
    }