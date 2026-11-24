"""API tests for the GitHub REST API using Playwright's APIRequestContext."""

import uuid

import pytest

pytestmark = [pytest.mark.api, pytest.mark.github]

REPO = "microsoft/playwright-python"


def test_github_repo_returns_expected_metadata(github):
    """Goal: verify GitHub repository metadata endpoint.
    Precondition: target repository is public.
    Expected: HTTP 200 with expected full_name, language Python, positive stars, and active status."""
    response = github.get(f"/repos/{REPO}")

    assert response.status == 200, response.text()
    body = response.json()
    assert body["full_name"] == REPO
    assert body["language"] == "Python"
    assert isinstance(body["stargazers_count"], int) and body["stargazers_count"] > 0
    assert body["archived"] is False


def test_github_unknown_user_returns_404(github):
    """Goal: verify GitHub returns 404 for nonexistent users.
    Precondition: a random login that does not exist.
    Expected: HTTP 404 with message 'Not Found'."""
    unknown_login = f"nonexistent-qa-{uuid.uuid4().hex[:12]}"
    response = github.get(f"/users/{unknown_login}")

    assert response.status == 404, response.text()
    assert response.json()["message"] == "Not Found"


def test_github_rate_limit_headers_are_valid(github):
    """Goal: verify GitHub responses include rate-limit headers.
    Precondition: GET /rate_limit does not consume quota.
    Expected: HTTP 200 with integer x-ratelimit-limit and x-ratelimit-remaining <= limit."""
    response = github.get("/rate_limit")

    assert response.status == 200, response.text()
    limit = int(response.headers["x-ratelimit-limit"])
    remaining = int(response.headers["x-ratelimit-remaining"])
    assert limit > 0
    assert 0 <= remaining <= limit
