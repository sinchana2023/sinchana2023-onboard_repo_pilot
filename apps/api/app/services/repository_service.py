import shutil
import subprocess
from pathlib import Path


class RepositoryService:
    REPOSITORY_ROOT = Path("/tmp/onboardai/repositories")

    @classmethod
    def clone_repository(
        cls,
        owner: str,
        repository: str,
    ) -> Path:
        cls.REPOSITORY_ROOT.mkdir(
            parents=True,
            exist_ok=True,
        )

        repository_path = cls.REPOSITORY_ROOT / f"{owner}_{repository}"

        if repository_path.exists():
            shutil.rmtree(repository_path)

        clone_url = (
            f"https://github.com/{owner}/{repository}.git"
        )

        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                clone_url,
                str(repository_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        return repository_path