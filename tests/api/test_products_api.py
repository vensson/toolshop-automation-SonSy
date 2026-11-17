
"""API tests for product listing, search, and error handling."""

import json
from pathlib import Path

import pytest


KEYWORDS = json.loads(
    (Path(__file__).parents[2] / "data" / "search_keywords.json")
    .read_text(encoding="utf-8")
)


@pytest.mark.api
def test_products_first_page_has_valid_json_structure(api):
    """Goal: validate GET /products response.
    Precondition: products API is available.
    Expected: pagination fields and valid product objects."""
    response = api.get("/products", params={"page": 1})

    assert response.status == 200, response.text()

    body = response.json()

    for key in ("current_page", "data", "per_page", "total", "last_page"):
        assert key in body, f"Missing key: {key}"

    assert 0 < len(body["data"]) <= body["per_page"]

    for product in body["data"]:
        assert isinstance(product["id"], (str, int))
        assert isinstance(product["name"], str)
        assert product["name"].strip()
        assert isinstance(product["price"], (int, float))
        assert product["price"] > 0


@pytest.mark.api
@pytest.mark.parametrize(
    "case",
    KEYWORDS,
    ids=[case["keyword"] for case in KEYWORDS],
)
def test_products_search_returns_matching_names(api, case):
    """Goal: verify product search.
    Precondition: search keywords loaded from JSON.
    Expected: every returned name contains the expected keyword."""
    response = api.get(
        "/products/search",
        params={"q": case["keyword"]},
    )

    assert response.status == 200, response.text()

    names = [
        product["name"]
        for product in response.json()["data"]
    ]

    assert names, f"No results for {case['keyword']}"

    assert all(
        case["must_contain"] in name.lower()
        for name in names
    ), names


@pytest.mark.api
@pytest.mark.parametrize(
    "path, expected",
    [
        ("/users/me", 401),
        ("/products/does-not-exist", 404),
    ],
)
def test_api_protected_or_missing_resource_returns_4xx(
    api, path, expected
):
    """Goal: verify API error handling.
    Precondition: request has no authentication token.
    Expected: protected or missing resources return 401 or 404."""
    response = api.get(path)

    assert response.status == expected, response.text()
