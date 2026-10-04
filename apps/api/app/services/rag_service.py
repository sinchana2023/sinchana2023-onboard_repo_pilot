from sqlalchemy.orm import Session

from app.services.llm_service import LLMService
from app.services.prompt_service import PromptService
from app.services.retrieval_service import RetrievalService


class RAGService:
    """Answer repository questions using retrieved evidence."""

    def __init__(
        self,
        retrieval_service: RetrievalService | None = None,
        llm_service: LLMService | None = None,
    ) -> None:
        self.retrieval_service = (
            retrieval_service
            or RetrievalService()
        )
        self.llm_service = (
            llm_service
            or LLMService()
        )

    def answer(
        self,
        repository_id: int,
        question: str,
        db: Session,
        top_k: int = 5,
    ) -> dict:
        """Answer a question using relevant repository chunks."""

        # 1. Retrieve the most relevant repository chunks.
        results = self.retrieval_service.search(
            repository_id=repository_id,
            query=question,
            db=db,
            top_k=top_k,
        )

        # 2. Refuse to answer when retrieval finds no evidence.
        if not results:
            return {
                "answer": (
                    "I couldn't find enough evidence in "
                    "the repository to answer this question."
                ),
                "sources": [],
            }

        # 3. Format the retrieved chunks as grounded context.
        user_prompt = PromptService.build_user_prompt(
            question=question,
            results=results,
        )

        # 4. Ask the LLM to answer using that context.
        answer = self.llm_service.generate(
            system_prompt=PromptService.SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        # 5. Return the answer with its supporting sources.
        sources = [
            {
                "path": result["path"],
                "start_line": result["start_line"],
                "end_line": result["end_line"],
                "score": result["score"],
            }
            for result in results
        ]

        return {
            "answer": answer,
            "sources": sources,
        }