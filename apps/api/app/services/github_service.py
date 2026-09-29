from urllib.parse import urlparse


class GitHubService:
    @staticmethod
    def parse_repository_url(github_url: str) -> tuple[str, str]:
        parsed = urlparse(github_url)

        if parsed.netloc.lower() not in {"github.com", "www.github.com"}:
            raise ValueError("URL must be a GitHub repository URL.")

        parts = [
            part
            for part in parsed.path.strip("/").split("/")
            if part
        ]

        if len(parts) < 2:
            raise ValueError("Invalid GitHub repository URL.")

        owner = parts[0]
        repository = parts[1]

        if repository.endswith(".git"):
            repository = repository[:-4]

        return owner, repository