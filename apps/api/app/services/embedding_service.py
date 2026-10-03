from openai import OpenAI

from app.core.config import settings


class EmbeddingService:
    """Generate embeddings for repository text."""

    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.openai_api_key
        )

        self.model = settings.embedding_model

    def embed_text(self, text: str) -> list[float]:
        """Generate an embedding for a single piece of text."""

        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embeddings for multiple pieces of text."""

        if not texts:
            return []

        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )

        return [
            item.embedding
            for item in response.data
        ]