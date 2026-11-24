
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import expect

from pages.home_page import HomePage

pytestmark = [pytest.mark.bdd, pytest.mark.ui]

scenarios("cart.feature")


@pytest.fixture
def cart_state():
    return {}


@given("I am browsing the product catalog")
def browse_catalog(page, cart_state):
    cart_state["home"] = HomePage(page).open()


@when(parsers.parse('I select the product "{product}"'))
def select_product(cart_state, product):
    detail = cart_state["home"].open_product(product)
    expect(detail.name).to_have_text(product)

    cart_state["product"] = detail
    cart_state["unit_price"] = detail.price()


@when(parsers.parse("I add the product with quantity {quantity:d}"))
def add_product(cart_state, quantity):
    detail = cart_state["product"]
    detail.add_to_cart(quantity=quantity)

    expect(detail.cart_quantity).to_have_text(str(quantity))
    cart_state["cart"] = detail.go_to_cart()


@then(parsers.parse('the cart should contain "{product}"'))
def verify_product(cart_state, product):
    cart = cart_state["cart"]
    expect(cart.product_titles.first).to_contain_text(product)


@then(
    parsers.parse(
        "the cart price should equal the unit price multiplied by {quantity:d}"
    )
)
def verify_price(cart_state, quantity):
    cart = cart_state["cart"]
    expected = round(cart_state["unit_price"] * quantity, 2)

    line_totals = cart.line_totals()
    assert len(line_totals) == 1
    assert abs(line_totals[0] - expected) < 0.01
    assert abs(cart.total_value() - expected) < 0.01
