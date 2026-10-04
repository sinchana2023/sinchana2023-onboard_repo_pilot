class PromptService:
    """Build grounded prompts from retrieved repository context."""

    SYSTEM_PROMPT = """
You are OnboardAI, an AI assistant that helps developers
understand unfamiliar software repositories.

Answer the user's question using ONLY the repository context
provided to you.

Do not invent:
- files
- functions
- classes
- behavior
- dependencies
- architecture

If the supplied context does not contain enough evidence,
say that you do not have enough evidence to answer the question.

When making a claim, cite the relevant source using its
provided file path and line range.
""".strip()

    @classmethod
    def build_user_prompt(
        cls,
        question: str,
        results: list[dict],
    ) -> str:
        """Format retrieved chunks as grounded LLM context."""

        context_blocks = []

        for index, result in enumerate(results, start=1):
            language = result["language"] or ""

            context_blocks.append(
                f"""
SOURCE {index}
File: {result["path"]}
Language: {result["language"] or "Unknown"}
Lines: {result["start_line"]}-{result["end_line"]}
Similarity: {result["score"]:.4f}

```{language}
{result["content"]}
```
""".strip()
            )

        context = "\n\n".join(context_blocks)

        return f"""
Repository context:

{context}

User question:
{question}

Answer using only the repository evidence above.
""".strip()