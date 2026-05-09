from freezegun import freeze_time


def test_register(client):

    response = client.post(
        "/auth/register",
        json={
            "email": "test@test.com",
            "username": "luiz",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "test@test.com"
    assert data["username"] == "luiz"


def test_login(login_response):

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_get_me(client, auth_headers):

    response = client.get(
        "/users/me",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "luiz@teste.com"
    assert data["username"] == "luiz"


def test_get_me_unauthorized(client):

    response = client.get("/users/me")

    assert response.status_code == 401


def test_login_wrong_password(client, registered_user):

    response = client.post(
        "/auth/login",
        json={
            "email": "luiz@teste.com",
            "password": "senha_errada",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid credentials"


def test_login_email_not_found(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "naoexiste@teste.com",
            "password": "123456",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid credentials"


def test_refresh_token(client, refresh_token):

    response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data


def test_logout(client, refresh_token):

    response = client.post(
        "/auth/logout",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 204


@freeze_time("2026-01-01 12:00:00")
def test_expired_token(client, access_token):

    with freeze_time("2026-01-01 13:00:00"):

        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 401

        data = response.json()

        assert data["detail"] == "Token expired"


@freeze_time("2026-01-01 12:00:00")
def test_expired_token(client):

    client.post(
        "/auth/register",
        json={
            "email": "luiz@teste.com",
            "username": "luiz",
            "password": "123456",
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "luiz@teste.com",
            "password": "123456",
        },
    )

    token = login_response.json()["access_token"]

    with freeze_time("2026-01-01 13:00:00"):

        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 401

        data = response.json()

        assert data["detail"] == "Token expired"


def test_invalid_token(client):

    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer token_fake"},
    )

    assert response.status_code == 401


def test_missing_bearer(client):

    response = client.get(
        "/users/me",
        headers={"Authorization": "token_sem_bearer"},
    )

    assert response.status_code == 401
