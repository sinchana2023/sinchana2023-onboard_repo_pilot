from openai import OpenAI

from app.core.config import settings


class LLMService:
    """Generate grounded answers using the configured LLM."""

    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.openai_api_key
        )

        self.model = settings.llm_model

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.choices[0].message.content or ""