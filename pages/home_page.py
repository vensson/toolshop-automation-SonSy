
import re

from pages.base_page import BasePage

# PROD uses QUERY /products.
# BUGGY uses GET /products?... .
PRODUCT_LIST = re.compile(r"/products(\?.*)?$")


class HomePage(BasePage):
    path = "/"

    def __init__(self, page):
        super().__init__(page)

        # Search
        self.search_box = page.get_by_test_id("search-query")
        self.search_result_count = page.get_by_test_id(
            "search-result-count"
        )
        self.search_button = page.get_by_test_id("search-submit")
        self.search_caption = page.get_by_test_id("search-caption")
        self.search_completed = page.get_by_test_id(
            "search_completed"
        )

        # Products
        self.product_names = page.get_by_test_id("product-name")
        self.product_prices = page.get_by_test_id("product-price")

        # No results
        self.no_results = page.get_by_test_id("no-results")

        # Sorting
        self.sort_select = page.get_by_test_id("sort")
        self.sorting_completed = page.get_by_test_id(
            "sorting_completed"
        )

        # Category filter
        self.category_hammer = page.get_by_label(
            "Hammer", exact=True
        )

    def open(self):
        """Open home and wait for the initial product API response."""
        with self.page.expect_response(
            lambda response:
                PRODUCT_LIST.search(response.url) is not None
        ):
            super().open()

        return self

    def search(self, keyword: str):
        self.search_box.fill(keyword)
        self.search_button.click()
        return self

    def sort_by(self, value: str):
        """Sort using name/price and asc/desc."""
        self.sort_select.select_option(value)
        return self

    def filter_hammers(self):
        """Select Hammer category and wait for the API response."""
        with self.page.expect_response(
            lambda response:
                PRODUCT_LIST.search(response.url) is not None
                and response.status == 200
        ):
            self.category_hammer.check()

        return self

    def product_card(self, name: str):
        return self.product_names.filter(
            has_text=re.compile(
                rf"^\s*{re.escape(name)}\s*$"
            )
        )

    def open_product(self, name: str):
        from pages.product_page import ProductPage

        self.product_card(name).click()
        return ProductPage(self.page)

    def prices(self) -> list[float]:
        return [
            float(price.replace("$", "").replace(",", ""))
            for price in self.product_prices.all_inner_texts()
        ]
