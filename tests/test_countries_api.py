import json
import logging
from pathlib import Path
from typing import Optional

import pandas as pd
import pytest

from restapi_framework import APIClient


def test_search_canada(countries_api_client: APIClient) -> None:
    response = countries_api_client.get("/countries/v5", params={"q": "canada"})

    assert response.status_code == 200, (
        f"Canada search failed with HTTP {response.status_code}."
    )
    countries = response.json()["data"]["objects"]
    assert isinstance(countries, list)
    assert countries
    canada = next(
        (country for country in countries if country["codes"]["alpha_2"] == "CA"),
        None,
    )
    assert canada is not None, "Search results did not contain Canada."
    assert canada["names"]["common"] == "Canada"
    assert canada["codes"]["alpha_3"] == "CAN"
    assert any(capital["name"] == "Ottawa" for capital in canada["capitals"])


@pytest.mark.parametrize("authorization", [None, "Bearer invalid-test-token"])
def test_countries_rejects_missing_or_invalid_token(
    countries_api_client: APIClient, authorization: Optional[str]
) -> None:
    response = countries_api_client.get(
        "/countries/v5",
        params={"q": "canada"},
        headers={"Authorization": authorization},
    )

    assert response.status_code in (401, 403), (
        "The endpoint did not reject missing or invalid Bearer authentication "
        f"(HTTP {response.status_code})."
    )

def test_search_canada_json_response(countries_api_client: APIClient) -> None:
    response = countries_api_client.get("/countries/v5", params={"q": "canada"})

    assert response.status_code == 200, (
        f"Canada search failed with HTTP {response.status_code}."
    )
    countries = response.json()
    
    logging.info(
    "Canada API response:\n%s",
    json.dumps(countries, indent=2, ensure_ascii=False),)

def test_search_canada_djsons(countries_api_client: APIClient) -> None:
    name={"russian": {"letters": ["a","b","c","d","e"]}}
    names= [name["russian"] for letter in name]
    logging.debug("Generated names: %s", name)
    rnames=None
    logging.debug("Generated names list: %s", names)
    logging.debug("Generated Russian letters list: %s", rnames)

@pytest.mark.parametrize("country_name", ["canada","japan","france","germany","india"])
def test_search_canada_dataframe(countries_api_client: APIClient, country_name: str) -> None:
    response = countries_api_client.get("/countries/v5", params={"q": country_name})
    assert response.status_code == 200, (
        f"{country_name} search failed with HTTP {response.status_code}."
    )
    countries = response.json()["data"]["objects"]
    assert isinstance(countries, list)
    assert countries, f"{country_name} search returned no country records."
    countries_df = pd.DataFrame([
        {
            "common": country["names"]["common"],
            "official": country["names"]["official"],
            "alpha_2": country["codes"]["alpha_2"],
            "alpha_3": country["codes"]["alpha_3"],
        }
        for country in countries
    ])
    assert countries_df["common"].str.casefold().eq(country_name.casefold()).any()

    logging.info(
        "Country summary for %s:\n%s",
        country_name,
        countries_df.to_string(index=False),
    )

 