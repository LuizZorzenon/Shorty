import pytest


@pytest.fixture
def registered_user(client):

    response = client.post(
        "/auth/register",
        json={
            "email": "luiz@teste.com",
            "username": "luiz",
            "password": "123456",
        },
    )

    return response.json()


@pytest.fixture
def login_response(client, registered_user):

    response = client.post(
        "/auth/login",
        json={
            "email": "luiz@teste.com",
            "password": "123456",
        },
    )

    return response


@pytest.fixture
def access_token(login_response):

    return login_response.json()["access_token"]


@pytest.fixture
def refresh_token(login_response):

    return login_response.json()["refresh_token"]


@pytest.fixture
def auth_headers(access_token):

    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def second_user(client):

    response = client.post(
        "/auth/register",
        json={
            "email": "segundo@teste.com",
            "username": "segundo",
            "password": "123456",
        },
    )

    return response.json()


@pytest.fixture
def second_user_token(client, second_user):

    response = client.post(
        "/auth/login",
        json={
            "email": "segundo@teste.com",
            "password": "123456",
        },
    )

    return response.json()["access_token"]


@pytest.fixture
def second_user_headers(second_user_token):

    return {"Authorization": f"Bearer {second_user_token}"}
