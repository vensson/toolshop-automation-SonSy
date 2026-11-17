
"""Sprint 2 - Network routing and API mocking tests."""

import json
import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


PRODUCT_LIST = re.compile(r"/products(\?.*)?$")

EMPTY_PAGE = {
    "current_page": 1,
    "data": [],
    "from": None,
    "last_page": 1,
    "per_page": 9,
    "to": None,
    "total": 0,
}


@pytest.mark.ui
def test_home_without_images_still_lists_products(page):
    """Goal: verify the page works without images.
    Precondition: image requests are blocked.
    Expected: product names remain visible and images are blocked."""

    blocked = []

    def block_images(route):
        blocked.append(route.request.url)
        route.abort()

    page.route(
        re.compile(r"\.(png|jpe?g|webp|avif|svg)(\?.*)?$"),
        block_images,
    )

    home = HomePage(page).open()

    expect(home.product_names.first).to_be_visible()

    assert blocked, "No image requests were blocked"


@pytest.mark.ui
def test_home_empty_product_list_shows_no_results(page):
    """Goal: verify the empty product list interface.
    Precondition: product API returns an empty list.
    Expected: no-results message and zero product cards."""

    page.route(
        PRODUCT_LIST,
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(EMPTY_PAGE),
        ),
    )

    home = HomePage(page).open()

    expect(home.no_results).to_have_text(
        "There are no products found."
    )

    expect(home.product_names).to_have_count(0)
