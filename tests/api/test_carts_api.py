
"""API tests for shopping cart operations."""

import pytest


@pytest.fixture
def new_cart(api):
    """Create a fresh shopping cart for each test."""
    response = api.post("/carts")

    assert response.status == 201, response.text()

    return response.json()["id"]


@pytest.mark.api
def test_cart_add_product_quantity_two_is_stored(api, new_cart):
    """Goal: verify cart item quantity.
    Precondition: a new cart and an existing product.
    Expected: cart stores exactly one item with quantity two."""

    response = api.get("/products", params={"page": 1})
    assert response.status == 200, response.text()

    product = response.json()["data"][0]

    added = api.post(
        f"/carts/{new_cart}",
        data={
            "product_id": product["id"],
            "quantity": 2,
        },
    )

    assert added.ok, added.text()

    cart_response = api.get(f"/carts/{new_cart}")
    assert cart_response.status == 200, cart_response.text()

    items = cart_response.json()["cart_items"]

    assert len(items) == 1
    assert items[0]["quantity"] == 2
    assert str(items[0]["product_id"]) == str(product["id"])
