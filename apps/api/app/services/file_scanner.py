from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".github",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".next",
    "dist",
    "build",
    "coverage",
}


SUPPORTED_EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".c": "C",
    ".cpp": "C++",
    ".cs": "C#",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".md": "Markdown",
}


MAX_FILE_SIZE = 500_000


class FileScanner:
    @staticmethod
    def scan(repository_path: Path) -> list[dict]:
        files = []

        for path in repository_path.rglob("*"):
            if not path.is_file():
                continue

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            if path.stat().st_size > MAX_FILE_SIZE:
                continue

            language = SUPPORTED_EXTENSIONS.get(
                path.suffix.lower()
            )

            if language is None:
                continue

            files.append(
                {
                    "path": path,
                    "relative_path": str(
                        path.relative_to(repository_path)
                    ),
                    "language": language,
                    "size_bytes": path.stat().st_size,
                }
            )

        return files