import pytest
import allure
from selene import browser
from allure_commons.types import AttachmentType
from api_client import ApiClient
from attach import add_screenshot

BASE_URL = "https://demowebshop.tricentis.com"
EMAIL = "tester_guru@gmail.com"
PASSWORD = "Test1234"


@pytest.fixture(scope="session")
def api() -> ApiClient:
    return ApiClient(BASE_URL)


@pytest.fixture(scope="function")
def logged_in_browser(api: ApiClient):
    browser.config.base_url = BASE_URL
    browser.config.window_width = 1280
    browser.config.window_height = 800

    with allure.step("Login via API and transfer cookie"):
        resp = api.post("/login", data={"Email": EMAIL, "Password": PASSWORD, "RememberMe": False},
                        allow_redirects=False)
        allure.attach(str(resp.status_code), "Login status", AttachmentType.TEXT)
        cookie = resp.cookies.get("NOPCOMMERCE.AUTH")
        assert cookie, "Auth cookie not received"

        browser.open("/")
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open("/")

    yield browser

    add_screenshot(browser)
    browser.quit()
