"""API tests for health status, catalog metadata, auth login, and cart mutations."""

import pytest

from conftest import new_email, register_user, strong_password


@pytest.mark.smoke
@pytest.mark.api
def test_status_returns_toolshop(api):
    """Goal: verify API service health status.
    Precondition: Toolshop API is reachable.
    Expected: HTTP 200 with app_name set to Toolshop."""
    response = api.get("/status")

    assert response.status == 200, response.text()
    assert response.json()["app_name"] == "Toolshop"


@pytest.mark.api
@pytest.mark.parametrize("endpoint", ["/categories", "/brands"])
def test_catalog_metadata_returns_valid_items(api, endpoint):
    """Goal: verify categories and brands catalog endpoints.
    Precondition: Toolshop API is reachable.
    Expected: HTTP 200 with a non-empty list of objects containing id, name, and slug."""
    response = api.get(endpoint)

    assert response.status == 200, response.text()
    items = response.json()
    assert isinstance(items, list) and items, f"Expected non-empty list from {endpoint}"

    for item in items:
        assert item.get("id")
        assert isinstance(item.get("name"), str) and item["name"].strip()
        assert isinstance(item.get("slug"), str) and item["slug"].strip()


@pytest.mark.api
def test_login_valid_user_returns_bearer_token(api, test_user):
    """Goal: verify user login returns a valid bearer token.
    Precondition: a fresh user account created by the test_user fixture.
    Expected: HTTP 200 with non-empty access_token and bearer token_type."""
    response = api.post(
        "/users/login",
        data={
            "email": test_user["email"],
            "password": test_user["password"],
        },
    )

    assert response.status == 200, response.text()
    body = response.json()
    assert body.get("access_token")
    assert body.get("token_type", "").lower() == "bearer"


@pytest.mark.api
def test_login_nonexistent_user_returns_401(api):
    """Goal: verify login rejects unknown credentials.
    Precondition: a freshly generated email not registered in Toolshop.
    Expected: HTTP 401 Unauthorized."""
    response = api.post(
        "/users/login",
        data={
            "email": new_email(),
            "password": "WrongPassword123!",
        },
    )

    assert response.status == 401, response.text()


@pytest.mark.api
def test_cart_update_quantity_and_remove_item(api):
    """Goal: verify cart item quantity update and item deletion via API.
    Precondition: a new cart and an existing product from GET /products.
    Expected: quantity updates to 3 and item is removed leaving an empty cart."""
    products_response = api.get("/products", params={"page": 1})
    assert products_response.status == 200, products_response.text()
    product_id = products_response.json()["data"][0]["id"]

    cart_response = api.post("/carts")
    assert cart_response.status == 201, cart_response.text()
    cart_id = cart_response.json()["id"]

    add_response = api.post(
        f"/carts/{cart_id}",
        data={"product_id": product_id, "quantity": 1},
    )
    assert add_response.ok, add_response.text()

    update_response = api.put(
        f"/carts/{cart_id}/product/quantity",
        data={"product_id": product_id, "quantity": 3},
    )
    assert update_response.status == 200, update_response.text()

    after_update = api.get(f"/carts/{cart_id}")
    assert after_update.status == 200, after_update.text()
    items = after_update.json()["cart_items"]
    assert len(items) == 1
    assert items[0]["quantity"] == 3

    delete_response = api.delete(f"/carts/{cart_id}/product/{product_id}")
    assert delete_response.status in (200, 204), delete_response.text()

    after_delete = api.get(f"/carts/{cart_id}")
    assert after_delete.status == 200, after_delete.text()
    assert after_delete.json()["cart_items"] == []


@pytest.mark.api
def test_users_register_leaked_password_returns_422(api):
    """Goal: verify registration rejects known leaked passwords.
    Precondition: a fresh email paired with a leaked password ('Welcome01!').
    Expected: HTTP 422 validation error."""
    response = register_user(api, new_email(), "Welcome01!")

    assert response.status == 422, response.text()


@pytest.mark.api
def test_users_register_response_does_not_expose_password(api):
    """Goal: verify registration response never leaks the user's password.
    Precondition: a fresh valid email and strong password.
    Expected: HTTP 201 and no 'password' key in the JSON response."""
    response = register_user(api, new_email(), strong_password())

    assert response.status == 201, response.text()
    assert "password" not in response.json()
