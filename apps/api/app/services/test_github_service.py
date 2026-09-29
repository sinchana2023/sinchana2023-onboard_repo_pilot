import pytest

from app.services.github_service import GitHubService


def test_parse_github_repository_url():
    owner, repository = GitHubService.parse_repository_url(
        "https://github.com/tiangolo/fastapi"
    )

    assert owner == "tiangolo"
    assert repository == "fastapi"


def test_parse_git_suffix():
    owner, repository = GitHubService.parse_repository_url(
        "https://github.com/tiangolo/fastapi.git"
    )

    assert owner == "tiangolo"
    assert repository == "fastapi"


def test_reject_non_github_url():
    with pytest.raises(ValueError):
        GitHubService.parse_repository_url(
            "https://gitlab.com/example/project"
        )