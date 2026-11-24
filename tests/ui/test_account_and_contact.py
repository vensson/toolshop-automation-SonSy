"""Regression UI tests for user login, account navigation, and contact submission."""

import re

import pytest
from playwright.sync_api import expect

from pages.account_page import AccountPage
from pages.contact_page import ContactPage
from pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.regression
def test_login_valid_user_redirects_to_account(page, test_user):
    """Goal: verify login with a valid account through the UI.
    Precondition: a registered user created by the test_user fixture.
    Expected: user is redirected to /account and sees the QA Bot menu."""
    login = LoginPage(page).open()

    login.login(email=test_user["email"], password=test_user["password"])

    expect(page).to_have_url(re.compile(r"/account$"))
    account = AccountPage(page)
    expect(account.title).to_have_text("My account")
    expect(account.nav_menu).to_contain_text("QA Bot")


@pytest.mark.ui
@pytest.mark.regression
def test_logged_in_account_navigates_to_profile_and_invoices(logged_in_page):
    """Goal: verify navigation links inside the authenticated account page.
    Precondition: user session is authenticated via auth_state.
    Expected: Profile and Invoices links route to their respective subpages."""
    account = AccountPage(logged_in_page).open()

    account.nav_profile.click()
    expect(logged_in_page).to_have_url(re.compile(r"/account/profile$"))

    account.open()
    account.nav_invoices.click()
    expect(logged_in_page).to_have_url(re.compile(r"/account/invoices$"))


@pytest.mark.ui
@pytest.mark.regression
def test_contact_valid_submission_shows_confirmation(page):
    """Goal: verify submitting the contact form with valid details.
    Precondition: the contact page is accessible.
    Expected: confirmation alert confirms the message was received."""
    contact = ContactPage(page).open()

    contact.fill_form(
        first="Hoang",
        last="Sy",
        email="qa-contact@example.com",
        subject="webmaster",
        message=(
            "This is a valid regression inquiry containing more than fifty "
            "characters for testing."
        ),
    ).submit()

    expect(contact.success).to_contain_text(
        "Thanks for your message! We will contact you shortly."
    )
