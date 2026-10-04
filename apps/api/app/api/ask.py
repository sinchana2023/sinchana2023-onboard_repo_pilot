from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.ask import AskRequest, AskResponse
from app.services.rag_service import RAGService


router = APIRouter(
    prefix="/api/v1/repositories",
    tags=["rag"],
)


@router.post(
    "/{repository_id}/ask",
    response_model=AskResponse,
)
def ask_repository(
    repository_id: int,
    request: AskRequest,
    db: Session = Depends(get_db),
):
    rag_service = RAGService()

    return rag_service.answer(
        repository_id=repository_id,
        question=request.question,
        db=db,
        top_k=request.top_k,
    )