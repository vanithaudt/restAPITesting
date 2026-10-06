import os
from collections.abc import Iterator

import pytest
from dotenv import load_dotenv

from restapi_framework import APIClient

load_dotenv()


@pytest.fixture
def api_client() -> Iterator[APIClient]:
    base_url = os.getenv("API_BASE_URL", "https://api.nasa.gov/neo/rest/v1/neo")
    timeout = float(os.getenv("API_TIMEOUT", "10"))
    api_key = os.getenv("API_KEY")
    if not api_key or api_key == "replace_with_your_api_key":
        raise pytest.UsageError("Set API_KEY in .env to a NASA API key.")
    client = APIClient(
        base_url, timeout=timeout, api_key=api_key, api_key_location="query"
    )
    try:
        yield client
    finally:
        client.session.close()


@pytest.fixture
def countries_api_client() -> Iterator[APIClient]:
    token = os.getenv("COUNTRIES_BEARER_TOKEN")
    if not token or token == "replace_with_your_bearer_token":
        raise pytest.UsageError("Set COUNTRIES_BEARER_TOKEN in .env.")
    client = APIClient(
        os.getenv("COUNTRIES_BASE_URL", "https://api.restcountries.com"),
        timeout=float(os.getenv("API_TIMEOUT", "10")),
        bearer_token=token,
    )
    try:
        yield client
    finally:
        client.session.close()
