import logging
from typing import Any, Literal, Optional
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests

logger = logging.getLogger(__name__)


class APIClient:
    """Small requests-based client for tests against a REST API."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        api_key: Optional[str] = None,
        api_key_location: Literal["header", "query"] = "header",
        bearer_token: Optional[str] = None,
    ) -> None:
        if api_key_location not in ("header", "query"):
            raise ValueError("api_key_location must be 'header' or 'query'.")
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout
        self.session = requests.Session()
        if bearer_token:
            self.session.headers["Authorization"] = f"Bearer {bearer_token}"
        if api_key:
            if api_key_location == "query":
                self.session.params["api_key"] = api_key
            else:
                self.session.headers["x-api-key"] = api_key

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = urljoin(self.base_url, path.lstrip("/"))
        parsed_url = urlsplit(url)
        safe_url = urlunsplit(
            (parsed_url.scheme, parsed_url.netloc, parsed_url.path, "", "")
        )
        logger.debug("Sending %s request to %s", method.upper(), safe_url)
        response = self.session.request(
            method,
            url,
            timeout=kwargs.pop("timeout", self.timeout),
            **kwargs,
        )
        logger.debug(
            "Received HTTP %s from %s (%.3f seconds)",
            response.status_code,
            safe_url,
            response.elapsed.total_seconds(),
        )
        return response

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)
