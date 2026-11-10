
"""Sprint 1 - Toolshop Automation Smoke Tests.

Run all smoke tests:
    pytest -m smoke -v

Rules:
- Locators must be defined in pages/, not in tests.
- Assertions must be defined in tests/, not in pages/.
- Do not use time.sleep() or wait_for_timeout().
"""

import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.login_page import LoginPage
from pages.contact_page import ContactPage


# ---------------------------------------------------------
# SMOKE 01 - SEARCH PRODUCT
# ---------------------------------------------------------

@pytest.mark.smoke
@pytest.mark.ui
def test_smoke_search_pliers(page):
    """Goal: search for products containing 'pliers'.
    Precondition: the home page is accessible.
    Expected: every displayed product name contains 'pliers'.
    """
    home = HomePage(page).open()

    home.search("pliers")

    expect(home.search_completed).to_be_visible()
    expect(home.search_caption).to_contain_text("pliers")

    product_names = home.product_names.all_inner_texts()

    assert product_names, "No products were found"

    assert all(
        "pliers" in name.lower()
        for name in product_names
    ), f"Unexpected search results: {product_names}"


# ---------------------------------------------------------
# SMOKE 02 - ADD PRODUCT TO CART
# ---------------------------------------------------------

@pytest.mark.smoke
@pytest.mark.ui
def test_smoke_add_claw_hammer_to_cart(page):
    """Goal: add three Claw Hammers to the cart.
    Precondition: Claw Hammer is available.
    Expected: the cart quantity badge displays 3.
    """
    home = HomePage(page).open()

    product = home.open_product("Claw Hammer")

    expect(product.name).to_have_text("Claw Hammer")

    product.add_to_cart(quantity=3)

    expect(product.toast).to_contain_text(
        "Product added to shopping cart"
    )

    expect(product.cart_quantity).to_have_text("3")


# ---------------------------------------------------------
# SMOKE 03 - INVALID LOGIN
# ---------------------------------------------------------

@pytest.mark.smoke
@pytest.mark.ui
def test_smoke_login_invalid_credentials(page):
    """Goal: reject login with invalid credentials.
    Precondition: the email does not belong to an account.
    Expected: an error appears and the user stays on login.
    """
    login = LoginPage(page).open()

    login.login(
        email="nobody-here@example.com",
        password="WrongPassword123!"
    )

    expect(login.error).to_contain_text(
        "Invalid email or password"
    )

    expect(page).to_have_url(
        re.compile(r"/auth/login$")
    )


# ---------------------------------------------------------
# SMOKE 04 - CONTACT FORM VALIDATION
# ---------------------------------------------------------

@pytest.mark.smoke
@pytest.mark.ui
def test_smoke_contact_empty_form(page):
    """Goal: validate required contact form fields.
    Precondition: the contact form is empty.
    Expected: subject and message required errors appear.
    """
    contact = ContactPage(page).open()

    contact.submit()

    error_messages = contact.errors.all_inner_texts()

    assert any(
        "Subject is required" in message
        for message in error_messages
    ), f"Subject validation error not found: {error_messages}"

    assert any(
        "Message is required" in message
        for message in error_messages
    ), f"Message validation error not found: {error_messages}"
