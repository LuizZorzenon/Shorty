def test_redirect_not_found(client):
    response = client.get("/abc123")

    assert response.status_code == 404
    assert response.json() == {"detail": "URL not found"}


def test_redirect_success(client, created_url):
    response = client.get(f"/{created_url['short_key']}", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "https://google.com/"
