from typing import Any, Optional
from urllib.parse import urljoin

import requests


class APIClient:
    """Small requests-based client for tests against a REST API."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        api_key: Optional[str] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout
        self.session = requests.Session()
        if api_key:
            self.session.headers["x-api-key"] = api_key

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = urljoin(self.base_url, path.lstrip("/"))
        return self.session.request(
            method,
            url,
            timeout=kwargs.pop("timeout", self.timeout),
            **kwargs,
        )

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)
