# toolshop-automation-SonSy

Automated UI, API, and network test suite for [Practice Software Testing (Toolshop)](https://practicesoftwaretesting.com) built with **Python**, **Playwright**, and **pytest**.

## Project Structure

```text
toolshop-automation-SonSy/
├── conftest.py        # Shared fixtures (api, github, test_user, auth_token, logged_in_page)
├── data/              # External test data (search_keywords.json)
├── pages/             # Page Object Model classes (locators and page actions)
├── tests/
│   ├── api/           # APIRequestContext tests (Toolshop API & GitHub REST API)
│   ├── bdd/           # Gherkin feature and pytest-bdd step definitions
│   └── ui/            # Smoke, regression, and network interception UI tests
├── pytest.ini         # Pytest configuration and custom markers
└── requirements.txt   # Pinned dependencies
```

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
```

## Running Tests

```bash
pytest -v
pytest -m smoke -v
pytest -m regression -v
pytest -m api -v
pytest -n auto
```

## Conventions

- **Page Object Model**: Locators live in `pages/`; assertions live in `tests/`.
- **No fixed sleeps**: Synchronize with `expect()` or `page.expect_response()`.
- **Isolated test accounts**: Tests create fresh accounts per session via `conftest.py` (`test_user`).
