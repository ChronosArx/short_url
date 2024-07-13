from fastapi.testclient import TestClient
from fastapi import status
from ..src.main import app
import re

client = TestClient(app)


def test_signup():
    response = client.post(
        "/apiv1/auth/signup",
        json={"user_name": "test", "email": "test@test.com", "password": "test123"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "access_token" in data


def test_login():
    response = client.post(
        "/apiv1/auth/login",
        json={"user_name": "test", "password": "test123"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    return data["access_token"]


def test_short_url():
    response = client.post(
        "/apiv1/shorten/shorten_url",
        json={"original_url": "http://example.com/example"},
    )
    assert response.status_code == 201

    # Verificar que el shorten_url tenga el formato esperado
    data = response.json()
    shorten_url = data.get("shorten_url")
    assert shorten_url is not None

    # Usar regex para verificar el formato de la URL
    pattern = re.compile(r"http://localhost/[a-zA-Z0-9]+")
    assert pattern.match(shorten_url)


def test_short_url_by_user():
    response = client.post(
        "/apiv1/shorten/shorten_url_by_user",
        json={
            "title": "title-test",
            "original_url": "http://test-example.com/test",
            "user": "test",
        },
        headers={"Authorization", f"Bearer {test_login}"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Verificar que el shorten_url tenga el formato esperado
    data = response.json()
    shorten_url = data.get("shorten_url")
    assert shorten_url is not None

    # Usar regex para verificar el formato de la URL
    pattern = re.compile(r"http://localhost/[a-zA-Z0-9]+")
    assert pattern.match(shorten_url)
