from datetime import datetime

from pydantic import BaseModel, HttpUrl


class RepositoryCreate(BaseModel):
    github_url: HttpUrl


class RepositoryResponse(BaseModel):
    id: int
    name: str
    github_url: str
    owner: str
    default_branch: str | None
    primary_language: str | None
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }