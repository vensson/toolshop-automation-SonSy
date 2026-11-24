
"""Sprint 2 - Network routing and API mocking tests."""

import json
import re

import pytest
from playwright.sync_api import expect

from pages.account_page import AccountPage
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


@pytest.mark.ui
@pytest.mark.regression
def test_home_when_product_api_fails_stays_usable(page):
    """Goal: verify UI resilience when the product list API returns HTTP 500.
    Precondition: GET/QUERY /products is mocked to return status 500.
    Expected: zero product cards render and the search box stays editable."""

    page.route(
        PRODUCT_LIST,
        lambda route: route.fulfill(
            status=500,
            content_type="application/json",
            body=json.dumps({"message": "Internal Server Error"}),
        ),
    )

    home = HomePage(page).open()

    expect(home.product_names).to_have_count(0)
    expect(home.search_box).to_be_editable()


@pytest.mark.ui
@pytest.mark.regression
def test_home_renders_price_from_api_response(page):
    """Goal: verify the UI displays prices directly from the API payload.
    Precondition: first product price in the real /products response is patched to 999.99.
    Expected: the first product card renders '$999.99'."""

    def patch_first_price(route):
        response = route.fetch()
        body = response.json()
        body["data"][0]["price"] = 999.99
        route.fulfill(response=response, json=body)

    page.route(PRODUCT_LIST, patch_first_price)

    home = HomePage(page).open()

    expect(home.product_prices.first).to_have_text("$999.99")


@pytest.mark.ui
@pytest.mark.regression
def test_account_page_with_token_injected_skips_login_form(page, auth_token):
    """Goal: verify API-assisted authentication by injecting auth-token into localStorage.
    Precondition: a valid bearer token from the auth_token fixture.
    Expected: AccountPage opens directly and displays the QA Bot user menu."""

    page.add_init_script(
        f"window.localStorage.setItem('auth-token', {json.dumps(auth_token)})"
    )

    account = AccountPage(page).open()

    expect(account.title).to_have_text("My account")
    expect(account.nav_menu).to_contain_text("QA Bot")
