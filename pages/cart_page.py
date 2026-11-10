
from pages.base_page import BasePage


def money(text: str) -> float:
    """'$28.30' -> 28.3"""
    return float(text.replace("$", "").replace(",", "").strip())


class CartPage(BasePage):
    path = "/checkout"

    def __init__(self, page):
        super().__init__(page)

        # B1.4: Cart locators
        self.product_titles = page.get_by_test_id("product-title")
        self.quantities = page.get_by_test_id("product-quantity")
        self.line_prices = page.get_by_test_id("line-price")
        self.total = page.get_by_test_id("cart-total")

        # B1.6: Continue shopping
        self.continue_shopping = page.get_by_test_id("continue-shopping")

    def line_totals(self):
      self.line_prices.first.wait_for(state="visible")
      texts = self.line_prices.all_text_contents()
      return [money(text) for text in texts]

    def total_value(self):
        return money(self.total.inner_text())
