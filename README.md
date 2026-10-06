# pytest REST API test framework

A small, reusable REST API testing starter built with pytest and Requests.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the example tests

The examples target NASA NeoWs `/browse` by default:

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

Pytest loads `.env` automatically. Set `API_KEY` to a NASA-issued API key
(a restful-api.dev key will not work). The NASA fixture sends it as the
`api_key` query parameter, not a Bearer token or `x-api-key` header.
Set `API_BASE_URL=https://api.nasa.gov/neo/rest/v1/neo` in `.env`.
Set `API_TIMEOUT` to override the request timeout in seconds (default: `10`).
The client still supports `x-api-key` authentication with its default
`api_key_location="header"` for other APIs.

## REST Countries Bearer authentication

The REST Countries tests run independently of the NASA tests. Set
`COUNTRIES_BASE_URL=https://api.restcountries.com` and
`COUNTRIES_BEARER_TOKEN` to your token in the Git-ignored `.env` file.
The `countries_api_client` fixture sends `Authorization: Bearer <token>`
without sending NASA's API key.

```bash
.venv/bin/python -m pytest -v tests/test_countries_api.py
```

The tests call `/countries/v5?q=canada`, check Canada's name, country codes,
and Ottawa capital, and verify rejection of missing or invalid tokens.
The reusable `APIClient` supports GET, POST, and generic `request` with
Bearer authentication by passing `bearer_token` to its constructor.
Tokens are not included in client logs.

To convert the response to a pandas DataFrame, run:

```bash
.venv/bin/python -m pytest -v tests/test_countries_api.py::test_search_canada_dataframe
```

This test is parameterized for Canada, India, and France. It creates and logs
a compact DataFrame with `common`, `official`, `alpha_2`, and `alpha_3` columns,
one row per returned country. Search results may include related countries or
territories; the test checks that the requested country is present.
Nested native names and translations are omitted from the summary. This test
does not export an Excel workbook.

## Logging level

Pytest automatically loads logging settings from `[tool.pytest.ini_options]`
in `pyproject.toml`. Change `log_cli_level` to `DEBUG` for detailed output,
or `INFO`, `WARNING`, or `ERROR` to reduce verbosity.
These settings apply to all loggers except `urllib3.connectionpool`, disabled
in `addopts` because its debug messages include URLs with secret query keys.
The API client logs request method and URL (without query parameters),
response status, and duration. It does not log headers or request/response
bodies.

```bash
.venv/bin/python -m pytest -v tests/test_rest_api.py::test_api_key_authentication
```

No `-s` or explicit logging loader is needed. To override the configured level
for a single run without editing the file:

```bash
.venv/bin/python -m pytest -v --log-cli-level=INFO tests/test_rest_api.py::test_api_key_authentication
```

### Terminal colors

Terminal output uses pytest's default color palette. No custom logging hooks
are needed; all logging settings are in `pyproject.toml`.
`--color=yes` in `addopts` enables colors; use `--color=no` to disable them.
Colors do not change level filtering: select `--log-cli-level=DEBUG` to see
all levels. Saved logs remain plain text.

### Saved logs

Pytest saves logs to `logs/pytest.log`, relative to the directory where you run
pytest, and automatically creates the folder if needed. All tests share this
file, including logging from setup, execution, and teardown.

The settings `log_file = "logs/pytest.log"` and `log_file_mode = "a"` in
`pyproject.toml` append logs across runs rather than overwriting them. Change
`log_file` to choose a different filename or use `log_file_mode = "w"` to
overwrite it each run. Change `log_file_level` to control saved log verbosity
independently of terminal logging. The `logs/` folder is ignored by Git. The
file contains logging messages, not captured `print()` output or a full pytest
report.

Log entries include the timestamp, level, logger name, and message. Test-name
labels and custom level colors require Python hooks and are not enabled in
this configuration-only setup. Existing saved log entries are unchanged.

## Add tests

Use the `api_client` pytest fixture in `tests/conftest.py`. It provides `get`,
`post`, and generic `request` methods, returns standard Requests responses, and
closes its session after each test.

```python
def test_health(api_client):
    response = api_client.get("/health")

    assert response.status_code == 200
```
