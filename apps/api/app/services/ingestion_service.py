"""Repository ingestion workflow orchestration."""

from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.services.code_processing_service import (
    CodeProcessingService,
)
from app.services.embedding_processor import (
    EmbeddingProcessor,
)
from app.services.file_scanner import FileScanner
from app.services.repository_analyzer import (
    RepositoryAnalyzer,
)
from app.services.repository_service import (
    RepositoryService,
)


class IngestionService:
    """Coordinate repository ingestion and embedding."""

    def __init__(
        self,
        embedding_processor: EmbeddingProcessor | None = None,
    ) -> None:
        self.embedding_processor = (
            embedding_processor
            or EmbeddingProcessor()
        )

    def ingest(
        self,
        repository: Repository,
        db: Session,
    ) -> Repository:
        """
        Clone, analyze, process, embed, and persist a repository.

        The workflow is:

        1. Mark repository as processing
        2. Clone repository
        3. Analyze repository
        4. Scan supported source files
        5. Persist repository metadata
        6. Create SourceFile and CodeChunk records
        7. Generate embeddings for every code chunk
        8. Mark repository as completed
        """

        repository.status = "processing"
        db.commit()
        db.refresh(repository)

        try:
            # 1. Clone repository.
            repository_path = (
                RepositoryService.clone_repository(
                    owner=repository.owner,
                    repository=repository.name,
                )
            )

            # 2. Analyze repository.
            analysis = RepositoryAnalyzer.analyze(
                repository_path
            )

            # 3. Scan supported source files.
            files = FileScanner.scan(
                repository_path
            )

            # 4. Store repository metadata.
            repository.local_path = str(repository_path)
            repository.file_count = len(files)
            repository.primary_language = analysis[
                "primary_language"
            ]

            # 5. Process source files into chunks.
            CodeProcessingService.process_repository(
                repository_id=repository.id,
                repository_path=repository_path,
                db=db,
            )

            # 6. Generate and store embeddings.
            self.embedding_processor.embed_repository(
                repository_id=repository.id,
                db=db,
            )

            # 7. Mark ingestion as complete.
            repository.status = "completed"

            db.commit()
            db.refresh(repository)

            return repository

        except Exception:
            db.rollback()

            repository.status = "failed"

            db.commit()
            db.refresh(repository)

            raise