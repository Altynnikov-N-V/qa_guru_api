import pytest
import allure


@allure.feature("HTTP Methods")
@allure.story("GET requests validation")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "get", "smoke")
@allure.title("GET / — Проверка главной страницы")
def test_get_homepage(api):
    with allure.step("Отправляем GET-запрос к главной странице"):
        resp = api.get("/")
    with allure.step("Проверяем статус-код и содержимое ответа"):
        assert resp.status_code == 200
        assert "Demo Web Shop" in resp.text


@allure.feature("HTTP Methods")
@allure.story("POST login with different credentials")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "post", "auth")
@allure.title("POST /login — Проверка авторизации с разными пользователями")
@pytest.mark.parametrize(
    "email,password,expected_status",
    [
        ("tester_guru@gmail.com", "Test1234", 302),  # корректные данные
        ("wrong_user@gmail.com", "Test1234", 200),  # неверный email
        ("tester_guru@gmail.com", "wrongpass", 200),  # неверный пароль
    ],
    ids=["valid", "invalid_email", "invalid_password"]
)
def test_post_login_with_params(api, email, password, expected_status):
    with allure.step(f"Отправляем POST-запрос на /login для {email}"):
        payload = {"Email": email, "Password": password, "RememberMe": False}
        resp = api.post("/login", data=payload, allow_redirects=False)

    with allure.step("Проверяем код ответа и содержимое"):
        assert resp.status_code == expected_status

        if resp.status_code == 302:
            allure.attach("Login successful", "Result", allure.attachment_type.TEXT)
        else:
            allure.attach(resp.text[:500], "Login page HTML", allure.attachment_type.TEXT)


@allure.feature("HTTP Methods")
@allure.story("DELETE cart operation")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("api", "delete", "regression")
@allure.title("DELETE /cart — Проверка удаления содержимого корзины")
def test_delete_cart(api):
    with allure.step("Отправляем DELETE-запрос на /cart"):
        resp = api.delete("/cart")

    with allure.step("Проверяем статус-код"):
        assert resp.status_code in (200, 302)


@allure.feature("Performance")
@allure.story("Response time check")
@allure.severity(allure.severity_level.TRIVIAL)
@allure.tag("api", "performance")
@allure.title("Проверка скорости ответа API (GET /)")
def test_response_time(api):
    with allure.step("Отправляем GET-запрос"):
        import time
        start = time.time()
        resp = api.get("/")
        elapsed = time.time() - start
    with allure.step("Проверяем, что ответ пришёл быстро"):
        assert resp.status_code == 200
        assert elapsed < 1.0, f"Response took too long: {elapsed:.2f}s"
