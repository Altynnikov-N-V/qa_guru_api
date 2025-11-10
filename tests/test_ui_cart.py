import allure
from selene import have

PRODUCT_ID = 31
PRODUCT_NAME = "14.1-inch Laptop"


@allure.feature("Cart")
@allure.story("Add product via API and verify via UI")
def test_add_product_via_api_and_check_ui(api, logged_in_browser):
    api.post(f"/addproducttocart/details/{PRODUCT_ID}/1", data={f"addtocart_{PRODUCT_ID}.EnteredQuantity": "1"})
    logged_in_browser.open('/cart')
    logged_in_browser.element('a.product-name').should(have.exact_text(PRODUCT_NAME))


@allure.feature("Cart")
@allure.story("Remove product and check empty UI")
def test_remove_product_via_ui(logged_in_browser):
    logged_in_browser.open('/cart')
    logged_in_browser.element('.qty-input').set_value('0')
    logged_in_browser.element('input[name="updatecart"]').click()
    logged_in_browser.element('.order-summary-content').should(have.text('Your Shopping Cart is empty!'))
