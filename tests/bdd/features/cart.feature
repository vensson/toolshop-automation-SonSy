
Feature: Calculate shopping cart prices
  As a shopper
  I want to add products in different quantities
  So that I can see the correct cart total

  Scenario Outline: Calculate the price of a product in the cart
    Given I am browsing the product catalog
    When I select the product "<product>"
    And I add the product with quantity <quantity>
    Then the cart should contain "<product>"
    And the cart price should equal the unit price multiplied by <quantity>

    Examples:
      | product      | quantity |
      | Claw Hammer  | 1        |
      | Claw Hammer  | 2        |
