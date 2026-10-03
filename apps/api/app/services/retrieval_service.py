from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.code_chunk import CodeChunk
from app.models.source_file import SourceFile
from app.services.embedding_service import EmbeddingService


class RetrievalService:
    """Retrieve repository chunks using semantic similarity."""

    MIN_SIMILARITY = 0.35

    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
    ) -> None:
        self.embedding_service = (
            embedding_service
            or EmbeddingService()
        )

    def search(
        self,
        repository_id: int,
        query: str,
        db: Session,
        top_k: int = 5,
    ) -> list[dict]:
        """Return semantically relevant repository chunks."""

        # Convert the user's query into an embedding.
        query_embedding = self.embedding_service.embed_text(
            query
        )

        # Calculate cosine distance.
        distance = CodeChunk.embedding.cosine_distance(
            query_embedding
        )

        # Retrieve candidate chunks.
        statement = (
            select(
                CodeChunk,
                SourceFile,
                distance.label("distance"),
            )
            .join(
                SourceFile,
                CodeChunk.source_file_id == SourceFile.id,
            )
            .where(
                CodeChunk.repository_id == repository_id,
                CodeChunk.embedding.is_not(None),
            )
            .order_by(distance)
            .limit(top_k)
        )

        rows = db.execute(statement).all()

        results = []

        for chunk, source_file, distance_value in rows:
            similarity = 1.0 - float(distance_value)

            # Ignore weak semantic matches.
            if similarity < self.MIN_SIMILARITY:
                continue

            results.append(
                {
                    "chunk_id": chunk.id,
                    "path": source_file.path,
                    "language": source_file.language,
                    "start_line": chunk.start_line,
                    "end_line": chunk.end_line,
                    "content": chunk.content,
                    "score": similarity,
                }
            )

        return results