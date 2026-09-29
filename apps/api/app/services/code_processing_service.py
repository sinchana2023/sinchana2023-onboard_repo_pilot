from pathlib import Path

from sqlalchemy.orm import Session

from app.models.code_chunk import CodeChunk
from app.models.source_file import SourceFile
from app.services.chunking_service import ChunkingService
from app.services.file_scanner import FileScanner


class CodeProcessingService:

    @staticmethod
    def process_repository(
        repository_id: int,
        repository_path: Path,
        db: Session,
    ) -> None:
        files = FileScanner.scan(repository_path)

        for file_info in files:
            try:
                content = file_info["path"].read_text(
                    encoding="utf-8"
                )
            except (UnicodeDecodeError, OSError):
                continue

            source_file = SourceFile(
                repository_id=repository_id,
                path=file_info["relative_path"],
                language=file_info["language"],
                size_bytes=file_info["size_bytes"],
            )

            db.add(source_file)
            db.flush()

            chunks = ChunkingService.chunk_text(content)

            for chunk in chunks:
                code_chunk = CodeChunk(
                    repository_id=repository_id,
                    source_file_id=source_file.id,
                    chunk_index=chunk["chunk_index"],
                    start_line=chunk["start_line"],
                    end_line=chunk["end_line"],
                    content=chunk["content"],
                )

                db.add(code_chunk)

        db.commit()