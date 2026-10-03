from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.code_chunk import CodeChunk
from app.services.embedding_service import EmbeddingService


class EmbeddingProcessor:
    """Generate and persist embeddings for code chunks."""

    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
    ) -> None:
        self.embedding_service = (
            embedding_service
            or EmbeddingService()
        )

    def embed_repository(
        self,
        repository_id: int,
        db: Session,
        batch_size: int = 50,
    ) -> int:
        """Embed all unembedded chunks for a repository."""

        chunks = list(
            db.scalars(
                select(CodeChunk)
                .where(
                    CodeChunk.repository_id == repository_id,
                    CodeChunk.embedding.is_(None),
                )
            )
        )

        total_embedded = 0

        for start in range(
            0,
            len(chunks),
            batch_size,
        ):
            batch = chunks[
                start : start + batch_size
            ]

            texts = [
                chunk.content
                for chunk in batch
            ]

            embeddings = (
                self.embedding_service.embed_batch(
                    texts
                )
            )

            for chunk, embedding in zip(
                batch,
                embeddings,
            ):
                chunk.embedding = embedding

            db.commit()

            total_embedded += len(batch)

        return total_embedded