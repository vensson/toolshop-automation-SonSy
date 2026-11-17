
"""API tests for user registration and authentication."""

import pytest


@pytest.mark.api
def test_users_register_empty_body_returns_422(api):
    """Goal: verify registration input validation.
    Precondition: registration request has an empty body.
    Expected: HTTP 422 with email and password errors."""
    response = api.post("/users/register", data={})

    assert response.status == 422, response.text()

    errors = response.json()

    assert "email" in errors
    assert "password" in errors


@pytest.mark.api
def test_users_me_with_token_returns_own_profile(
    api, auth_headers, test_user
):
    """Goal: verify authenticated user profile access.
    Precondition: a registered user and valid bearer token.
    Expected: HTTP 200 and matching email address."""
    response = api.get(
        "/users/me",
        headers=auth_headers,
    )

    assert response.status == 200, response.text()

    body = response.json()

    assert body["email"] == test_user["email"]
