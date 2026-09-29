class ChunkingService:
    CHUNK_SIZE = 80
    CHUNK_OVERLAP = 15

    @classmethod
    def chunk_text(cls, content: str) -> list[dict]:
        lines = content.splitlines()
        chunks = []

        start = 0
        chunk_index = 0

        while start < len(lines):
            end = min(
                start + cls.CHUNK_SIZE,
                len(lines),
            )

            chunk_lines = lines[start:end]
            chunk_content = "\n".join(chunk_lines).strip()

            if chunk_content:
                chunks.append(
                    {
                        "chunk_index": chunk_index,
                        "start_line": start + 1,
                        "end_line": end,
                        "content": chunk_content,
                    }
                )

                chunk_index += 1

            if end == len(lines):
                break

            start = end - cls.CHUNK_OVERLAP

        return chunks