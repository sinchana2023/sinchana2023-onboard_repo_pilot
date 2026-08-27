from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate, RepositoryResponse


router = APIRouter(
    prefix="/api/v1/repositories",
    tags=["repositories"],
)


@router.post(
    "",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_repository(
    repository_data: RepositoryCreate,
    db: Session = Depends(get_db),
):
    repository = Repository(
        name="pending",
        github_url=str(repository_data.github_url),
        owner="pending",
        status="pending",
    )

    db.add(repository)
    db.commit()
    db.refresh(repository)

    return repository