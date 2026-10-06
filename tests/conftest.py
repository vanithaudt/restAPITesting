import os
from collections.abc import Iterator

import pytest
from dotenv import load_dotenv

from restapi_framework import APIClient

load_dotenv()


@pytest.fixture
def api_client() -> Iterator[APIClient]:
    base_url = os.getenv("API_BASE_URL", "https://api.restful-api.dev")
    timeout = float(os.getenv("API_TIMEOUT", "10"))
    client = APIClient(base_url, timeout=timeout, api_key=os.getenv("API_KEY"))
    yield client
    client.session.close()
