# pytest REST API test framework

A small, reusable REST API testing starter built with pytest and Requests.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the example tests

The examples target the restful-api.dev objects endpoint by default:

```bash
pytest
```

Copy `.env.example` to `.env` and put your key in the `API_KEY` entry. The
`.env` file is ignored by Git so the key stays local:

```bash
cp .env.example .env
# Edit .env and replace the placeholder API_KEY value.
pytest
```

Pytest loads `.env` automatically, and the client sends the key in the
`x-api-key` header. To target another API, set `API_BASE_URL` in `.env` or the
shell. Set `API_TIMEOUT` to override the request timeout in seconds (default:
`10`).

## Add tests

Use the `api_client` pytest fixture in `tests/conftest.py`. It provides `get`,
`post`, and generic `request` methods, returns standard Requests responses, and
closes its session after each test.

```python
def test_health(api_client):
    response = api_client.get("/health")

    assert response.status_code == 200
```
