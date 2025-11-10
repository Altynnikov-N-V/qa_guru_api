import json
from urllib.parse import urljoin
import requests
import allure
from allure_commons.types import AttachmentType
from logging_session import LoggingSession


class ApiClient:
    """HTTP-клиент c базовым URL и относительными endpoint'ами"""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/') + '/'
        self.session: requests.Session = LoggingSession()
        self.session.verify = False

    def _full_url(self, endpoint: str) -> str:
        endpoint = endpoint.lstrip('/')
        return urljoin(self.base_url, endpoint)

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        url = self._full_url(endpoint)
        with allure.step(f"GET {endpoint}"):
            resp = self.session.get(url, **kwargs)
            self._attach_response(resp)
            return resp

    def post(self, endpoint: str, *, data=None, json_body=None, **kwargs) -> requests.Response:
        url = self._full_url(endpoint)
        with allure.step(f"POST {endpoint}"):
            if json_body is not None:
                kwargs.setdefault("headers", {}).update({"Content-Type": "application/json"})
                allure.attach(json.dumps(json_body, ensure_ascii=False, indent=2), "Request JSON", AttachmentType.JSON)
            if data is not None:
                allure.attach(json.dumps(data, ensure_ascii=False, indent=2), "Request FORM", AttachmentType.JSON)
            resp = self.session.post(url, json=json_body, data=data, **kwargs)
            self._attach_response(resp)
            return resp

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        url = self._full_url(endpoint)
        with allure.step(f"DELETE {endpoint}"):
            resp = self.session.delete(url, **kwargs)
            self._attach_response(resp)
            return resp

    @staticmethod
    def _attach_response(response: requests.Response):
        try:
            payload = response.json()
            allure.attach(json.dumps(payload, ensure_ascii=False, indent=2), f"Response JSON [{response.status_code}]",
                          AttachmentType.JSON)
        except Exception:
            allure.attach(response.text[:2000], f"Response TEXT [{response.status_code}]", AttachmentType.TEXT)
