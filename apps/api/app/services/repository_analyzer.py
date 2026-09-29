from collections import Counter
from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".next",
    "venv",
    ".venv",
    "__pycache__",
}


LANGUAGE_BY_EXTENSION = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
}


class RepositoryAnalyzer:
    @staticmethod
    def analyze(repository_path: Path) -> dict:
        language_counts = Counter()
        file_count = 0

        for path in repository_path.rglob("*"):
            if not path.is_file():
                continue

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            file_count += 1

            language = LANGUAGE_BY_EXTENSION.get(
                path.suffix.lower()
            )

            if language:
                language_counts[language] += 1

        primary_language = (
            language_counts.most_common(1)[0][0]
            if language_counts
            else None
        )

        return {
            "file_count": file_count,
            "primary_language": primary_language,
            "language_counts": dict(language_counts),
        }