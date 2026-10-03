from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str
    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class SearchResult(BaseModel):
    chunk_id: int
    path: str
    language: str | None
    start_line: int
    end_line: int
    content: str
    score: float


class SearchResponse(BaseModel):
    results: list[SearchResult]