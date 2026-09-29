import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate, RepositoryResponse
from app.services.github_service import GitHubService
from app.services.ingestion_service import IngestionService


logger = logging.getLogger(__name__)

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
    # 1. Parse and validate GitHub URL.
    try:
        owner, repository_name = GitHubService.parse_repository_url(
            str(repository_data.github_url)
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # 2. Create the initial database record.
    repository = Repository(
        name=repository_name,
        github_url=str(repository_data.github_url),
        owner=owner,
        status="pending",
    )

    db.add(repository)

    try:
        db.commit()
        db.refresh(repository)

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Repository already exists.",
        ) from exc

    # 3. Run the ingestion pipeline.
    try:
        ingestion_service = IngestionService()

        repository = ingestion_service.ingest(
            repository=repository,
            db=db,
        )

    except Exception as exc:
        logger.exception(
            "Repository ingestion failed for %s/%s",
            owner,
            repository_name,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Repository ingestion failed: {exc}",
        ) from exc

    return repository