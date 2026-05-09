def test_create_url(client, auth_headers):

    response = client.post(
        "/urls/",
        json={"original_url": "https://google.com"},
        headers=auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["original_url"].startswith("https://google.com")
    assert "short_key" in data


def test_list_urls(client, auth_headers, created_url):

    response = client.get(
        "/urls/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["original_url"].startswith("https://google.com")


def test_get_url_by_shortkey(
    client,
    auth_headers,
    created_url,
):

    response = client.get(
        f"/urls/{created_url['short_key']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["original_url"].startswith("https://google.com")


def test_update_url(client, auth_headers, created_url):

    response = client.patch(
        f"/urls/{created_url['short_key']}",
        json={"original_url": "https://youtube.com"},
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["original_url"].startswith("https://youtube.com")


def test_delete_url(client, auth_headers, created_url):

    response = client.delete(
        f"/urls/{created_url['short_key']}",
        headers=auth_headers,
    )

    assert response.status_code == 200


def test_get_deleted_url(
    client,
    auth_headers,
    created_url,
):

    client.delete(
        f"/urls/{created_url['short_key']}",
        headers=auth_headers,
    )

    response = client.get(
        f"/urls/{created_url['short_key']}",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_redirect_increments_clicks(client, created_url, auth_headers):

    client.get(f"/{created_url['short_key']}")

    response = client.get(
        f"/urls/{created_url['short_key']}",
        headers=auth_headers,
    )

    data = response.json()

    assert data["clicks"] == 1


def test_redirect_disabled_url(
    client,
    auth_headers,
    created_url,
):

    client.patch(
        f"/urls/{created_url['short_key']}",
        json={"is_active": False},
        headers=auth_headers,
    )

    response = client.get(f"/{created_url['short_key']}")

    assert response.status_code == 410


def test_cannot_access_other_user_url(
    client,
    created_url,
    second_user_headers,
):

    response = client.get(
        f"/urls/{created_url['short_key']}",
        headers=second_user_headers,
    )

    assert response.status_code == 403


def test_cannot_update_other_user_url(
    client,
    created_url,
    second_user_headers,
):

    response = client.patch(
        f"/urls/{created_url['short_key']}",
        json={"original_url": "https://youtube.com"},
        headers=second_user_headers,
    )

    assert response.status_code == 403


def test_cannot_delete_other_user_url(
    client,
    created_url,
    second_user_headers,
):

    response = client.delete(
        f"/urls/{created_url['short_key']}",
        headers=second_user_headers,
    )

    assert response.status_code == 403
