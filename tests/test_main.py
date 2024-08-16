from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.dependencies import get_db
from app.core.config_data_base import Base
from app.utils.generate_token import generate_token
import re


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

token = generate_token(1, "test")


def test_signup():
    response = client.post(
        "/apiv1/auth/signup",
        json={"username": "test", "email": "test@test.com", "password": "test123"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "access_token" in data


def test_login():
    response = client.post(
        "/apiv1/auth/login",
        data={"username": "test", "password": "test123"},
    )
    data = response.json()
    print(data)
    token = data.get("access_token")
    assert token is not None
    assert response.status_code == status.HTTP_200_OK


def test_get_token_with_refresh_token():
    login_data = {"username": "test", "password": "test123"}

    # Realiza el login y guarda las cookies
    response = client.post("/apiv1/auth/login", data=login_data)
    assert response.status_code == 200

    refresh_token = response.cookies.get("refresh_token")
    assert refresh_token is not None

    # Establece el refresh_token en el cliente antes de hacer la solicitud
    client.cookies.set("refresh_token", refresh_token)

    # Realiza la solicitud para obtener un nuevo access_token
    response = client.get("apiv1/auth/token")

    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response


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
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    # Verificar que el shorten_url tenga el formato esperado
    data = response.json()
    shorten_url = data.get("shorten_url")
    assert shorten_url is not None

    # Usar regex para verificar el formato de la URL
    pattern = re.compile(r"http://localhost/[a-zA-Z0-9]+")
    assert pattern.match(shorten_url)
