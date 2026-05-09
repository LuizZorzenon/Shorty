import pytest


@pytest.fixture
def created_url(client, auth_headers):

    response = client.post(
        "/urls/",
        json={"original_url": "https://google.com"},
        headers=auth_headers,
    )

    return response.json()

