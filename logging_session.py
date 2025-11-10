import json
import logging
import time
import requests
from termcolor import colored
from allure_commons.types import AttachmentType
import allure

# Глобальный логгер с датой, временем, уровнем и сообщением
_logger = logging.getLogger("api")
if not _logger.handlers:
    _logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    _logger.addHandler(handler)


class LoggingSession(requests.Session):
    """Session с красивым логом: уровень, дата/время, код ответа, client url"""

    def request(self, method, url, **kwargs):
        start = time.time()
        method = method.upper()
        _logger.info(colored(f"{method} {url}", "cyan"))

        with allure.step(f"{method} {url}"):
            try:
                resp = super().request(method, url, **kwargs)
                elapsed = round(time.time() - start, 3)
                _logger.info(colored(f"status={resp.status_code} time={elapsed}s", "green"))

                # Allure вложения
                try:
                    allure.attach(
                        json.dumps(resp.json(), ensure_ascii=False, indent=2),
                        f"Response JSON [{resp.status_code}]",
                        AttachmentType.JSON
                    )
                except Exception:
                    allure.attach(
                        resp.text[:2000],
                        f"Response TEXT [{resp.status_code}]",
                        AttachmentType.TEXT
                    )

                return resp

            except Exception as e:
                _logger.exception("Request failed")
                allure.attach(str(e), "Request Exception", AttachmentType.TEXT)
                raise
