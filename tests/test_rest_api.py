from restapi_framework import APIClient


def test_list_objects(api_client: APIClient) -> None:
    response = api_client.get("/browse")

    assert response.status_code == 200
    objects = response.json()
    assert isinstance(objects, dict)
    assert isinstance(objects["near_earth_objects"], list)
    assert objects["near_earth_objects"]
    assert all(isinstance(item, dict) for item in objects["near_earth_objects"])
    assert isinstance(objects["page"], dict)
    assert isinstance(objects["links"], dict)


def test_api_key_authentication(api_client: APIClient) -> None:
    response = api_client.get("/browse")

    assert response.status_code == 200, (
        "NASA /browse did not accept the configured NASA "
        f"API key (HTTP {response.status_code})."
    )

def test_invalid_api_key_is_rejected(api_client: APIClient) -> None:
    response = api_client.get("/browse", params={"api_key": "invalid-test-key"})
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "API_KEY_INVALID"

