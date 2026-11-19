import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

import database
from database import Base, get_db

os.makedirs("./test_data", exist_ok=True)

from main import app


@pytest.fixture()
def client():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestSession = sessionmaker(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_register_login_and_recipe_crud(client):
    register = client.post("/register", json={"email": "Cook@Example.com", "password": "password123"})
    assert register.status_code == 201

    conflict = client.post("/register", json={"email": "cook@example.com", "password": "password456"})
    assert conflict.status_code == 409

    login = client.post("/login", json={"email": "cook@example.com", "password": "password123"})
    assert login.status_code == 200

    bad_login = client.post("/login", json={"email": "cook@example.com", "password": "wrong"})
    assert bad_login.status_code == 401

    created = client.post("/recipes", json={
        "title": "Chicken Soup",
        "description": "A simple soup",
        "ingredients": "chicken, stock, salt",
        "steps": "Boil and season",
    })
    assert created.status_code == 201

    recipe_id = created.json()["id"]
    assert client.get("/recipes").status_code == 200
    assert client.get("/recipes", params={"search": "chicken"}).status_code == 200
    assert client.get(f"/recipes/{recipe_id}").status_code == 200

    updated = client.put(f"/recipes/{recipe_id}", json={
        "title": "Chicken Noodle Soup",
        "description": "Comfort food",
        "ingredients": "chicken, noodles, stock",
        "steps": "Boil, add noodles, season",
    })
    assert updated.status_code == 200

    deleted = client.delete(f"/recipes/{recipe_id}")
    assert deleted.status_code == 204
    assert client.get(f"/recipes/{recipe_id}").status_code == 404
