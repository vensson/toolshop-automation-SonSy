
"""Sprint 2 - UI regression tests for Toolshop."""

import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.account_page import AccountPage


# =========================================================
# TEST 01 - SEARCH UNKNOWN KEYWORD
# =========================================================

@pytest.mark.ui
@pytest.mark.regression
def test_search_unknown_keyword_shows_no_results(page):
    """Goal: search for a nonexistent product.
    Precondition: home page is available.
    Expected: no-results message appears."""

    home = HomePage(page).open()

    home.search("xyznonexistent123")

    expect(home.no_results).to_be_visible()
    expect(home.product_names).to_have_count(0)


# =========================================================
# TEST 02 - SORT PRODUCTS BY PRICE
# =========================================================

@pytest.mark.ui
@pytest.mark.regression
def test_sort_products_by_price_ascending(page):
    """Goal: sort products by ascending price.
    Precondition: product listing is available.
    Expected: displayed prices are in ascending order."""

    home = HomePage(page).open()

    home.sort_by("price,asc")

    expect(home.sorting_completed).to_be_visible()

    prices = home.prices()

    assert prices, "No product prices found"
    assert prices == sorted(prices), (
        f"Prices are not sorted correctly: {prices}"
    )


# =========================================================
# TEST 03 - FILTER HAMMER CATEGORY (DEBUG)
# =========================================================

@pytest.mark.ui
@pytest.mark.regression
def test_filter_hammer_category_shows_matching_products(page):
    """Goal: inspect Hammer category filtering.
    Precondition: product categories are available.
    Expected: filtered products match the Hammer category."""

    home = HomePage(page).open()

    home.filter_hammers()

    expect(home.category_hammer).to_be_checked()
    expect(home.product_names.first).to_be_visible()

    names = home.product_names.all_inner_texts()

    print("\n========== HAMMER FILTER RESULTS ==========")

    for index, name in enumerate(names, start=1):
        print(f"{index}. {name}")

    print(f"Total products: {len(names)}")
    print("===========================================")

    assert names, "No products found after filtering"

    assert all(
        "hammer" in name.lower()
        for name in names
    ), f"Unexpected products after Hammer filtering: {names}"


# =========================================================
# TEST 04 - PRODUCT DETAIL
# =========================================================

@pytest.mark.ui
@pytest.mark.regression
def test_product_detail_shows_correct_name_and_price(page):
    """Goal: verify product detail information.
    Precondition: Claw Hammer is available.
    Expected: correct name and positive price."""

    home = HomePage(page).open()

    product = home.open_product("Claw Hammer")

    expect(product.name).to_have_text("Claw Hammer")
    expect(product.unit_price).to_be_visible()

    assert product.price() > 0, (
        "Product price must be greater than zero"
    )


# =========================================================
# TEST 05 - CART LINE PRICE
# =========================================================

@pytest.mark.ui
@pytest.mark.regression
def test_cart_line_price_matches_quantity_times_unit_price(page):
    """Goal: verify cart line price calculation.
    Precondition: Claw Hammer is available.
    Expected: line price equals unit price times quantity."""

    home = HomePage(page).open()

    product = home.open_product("Claw Hammer")

    unit_price = product.price()

    product.add_to_cart(quantity=2)

    expect(product.cart_quantity).to_have_text("2")

    cart = product.go_to_cart()

    expect(cart.product_titles.first).to_contain_text(
        "Claw Hammer"
    )

    line_totals = cart.line_totals()

    assert len(line_totals) == 1, (
        f"Expected 1 cart item, found {len(line_totals)}"
    )

    expected_total = unit_price * 2
    actual_total = line_totals[0]

    assert abs(actual_total - expected_total) < 0.01, (
        f"Expected {expected_total}, got {actual_total}"
    )


# =========================================================
# TEST 06 - CONTINUE SHOPPING
# =========================================================

@pytest.mark.ui
@pytest.mark.regression
def test_cart_continue_shopping_returns_home(page):
    """Goal: verify continue shopping navigation.
    Precondition: cart contains a product.
    Expected: continue shopping returns to product listing."""

    home = HomePage(page).open()

    product = home.open_product("Claw Hammer")

    product.add_to_cart()

    cart = product.go_to_cart()

    expect(cart.continue_shopping).to_be_visible()

    cart.continue_shopping.click()

    expect(page).to_have_url(re.compile(r"/$"))

    expect(
        HomePage(page).product_names.first
    ).to_be_visible()


# =========================================================
# TEST 07 - LOGIN FORM VALIDATION
# =========================================================

@pytest.mark.ui
@pytest.mark.regression
def test_login_empty_form_shows_required_errors(page):
    """Goal: verify login form validation.
    Precondition: login form is empty.
    Expected: email and password required errors appear."""

    login = LoginPage(page).open()

    login.submit_button.click()

    expect(login.email_error).to_be_visible()
    expect(login.password_error).to_be_visible()


# =========================================================
# TEST 08 - LOGGED IN ACCOUNT
# =========================================================

@pytest.mark.ui
@pytest.mark.regression
def test_logged_in_account_displays_user_menu(logged_in_page):
    """Goal: verify saved authentication state.
    Precondition: auth_state logs in once per session.
    Expected: account page and QA Bot menu are visible."""

    account = AccountPage(logged_in_page).open()

    expect(account.title).to_have_text("My account")

    expect(account.nav_menu).to_contain_text("QA Bot")
