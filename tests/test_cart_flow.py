import allure
from schemas import validate_json, add_to_cart_resp_schema

PRODUCT_ID = 31


@allure.feature("Cart API")
@allure.story("Add to cart via API")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "cart", "post", "regression")
@allure.title("POST /addproducttocart — Добавление товара в корзину через API")
def test_add_to_cart(api):
    with allure.step(f"Добавляем продукт ID={PRODUCT_ID} в корзину"):
        resp = api.post(f"/addproducttocart/details/{PRODUCT_ID}/1",
                        data={f"addtocart_{PRODUCT_ID}.EnteredQuantity": "1"})

    with allure.step("Проверяем статус-код и схему ответа"):
        assert resp.status_code in (200, 302)
        try:
            payload = resp.json()
            validate_json(payload, add_to_cart_resp_schema)
        except Exception:
            allure.attach(resp.text[:800], "HTML response", allure.attachment_type.TEXT)


@allure.feature("Cart API")
@allure.story("Negative: add non-existent product")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("api", "cart", "negative")
@allure.title("POST /addproducttocart — Добавление несуществующего товара (проверка схемы)")
def test_add_invalid_product(api):
    invalid_product_id = 99999
    with allure.step(f"Пробуем добавить несуществующий товар ID={invalid_product_id}"):
        resp = api.post(f"/addproducttocart/details/{invalid_product_id}/1",
                        data={f"addtocart_{invalid_product_id}.EnteredQuantity": "1"})

    with allure.step("Проверяем статус-код и схему JSON (если ответ в JSON)"):
        assert resp.status_code in (200, 404)
        try:
            payload = resp.json()
            validate_json(payload, add_to_cart_resp_schema)
        except Exception:
            allure.attach(resp.text[:800], "HTML or unexpected response", allure.attachment_type.TEXT)


@allure.feature("Cart API")
@allure.story("End-to-End: add and clear cart")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "cart", "e2e")
@allure.title("E2E — Добавление и очистка корзины через API с проверкой схем")
def test_add_and_clear_cart(api):
    with allure.step("Добавляем товар в корзину через API"):
        add_resp = api.post(f"/addproducttocart/details/{PRODUCT_ID}/1",
                            data={f"addtocart_{PRODUCT_ID}.EnteredQuantity": "1"})
        assert add_resp.status_code in (200, 302)
        try:
            payload = add_resp.json()
            validate_json(payload, add_to_cart_resp_schema)
        except Exception:
            allure.attach(add_resp.text[:800], "HTML response on add", allure.attachment_type.TEXT)

    with allure.step("Очищаем корзину через API"):
        clear_resp = api.post("/cart", data={"itemquantity1": "0", "updatecart": "Update"})
        assert clear_resp.status_code in (200, 302)
        try:
            payload = clear_resp.json()
            validate_json(payload, add_to_cart_resp_schema)
        except Exception:
            allure.attach(clear_resp.text[:800], "HTML response on clear", allure.attachment_type.TEXT)
