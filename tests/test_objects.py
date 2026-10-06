from restapi_framework import APIClient


def test_list_objects(api_client: APIClient) -> None:
    response = api_client.get("/objects")

    assert response.status_code == 200
    objects = response.json()
    assert isinstance(objects, list)
    assert all(isinstance(item, dict) for item in objects)


def test_api_key_authentication(api_client: APIClient) -> None:
    assert api_client.session.headers.get("x-api-key"), (
        "API_KEY is not configured. Add it to the project .env file."
    )
    print("api key passed ")
    response = api_client.get("/collections")
    print("api collection received passed ")

    assert response.status_code == 200, (
        "The authenticated /collections endpoint did not accept the configured "
        f"API key (HTTP {response.status_code})."
    )
