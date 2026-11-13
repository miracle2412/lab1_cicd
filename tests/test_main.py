from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "REST API is working"}


def test_get_items():
    response = client.get("/api/items")
    assert response.status_code == 200


def test_create_item():
    response = client.post(
        "/api/items",
        json={"name": "Keyboard", "price": 50.0}
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Keyboard"
    assert response.json()["price"] == 50.0


def test_get_item():
    create_response = client.post(
        "/api/items",
        json={"name": "Laptop", "price": 1200.0}
    )
    assert create_response.status_code == 201

    item_id = create_response.json()["id"]

    response = client.get(f"/api/items/{item_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"
    assert response.json()["price"] == 1200.0


def test_update_item():
    create_response = client.post(
        "/api/items",
        json={"name": "Laptop", "price": 1200.0}
    )
    assert create_response.status_code == 201

    item_id = create_response.json()["id"]

    response = client.put(
        f"/api/items/{item_id}",
        json={"name": "Gaming Laptop", "price": 1500.0}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Gaming Laptop"
    assert response.json()["price"] == 1500.0


def test_delete_item():
    create_response = client.post(
        "/api/items",
        json={"name": "Mouse", "price": 25.0}
    )
    assert create_response.status_code == 201

    item_id = create_response.json()["id"]

    response = client.delete(f"/api/items/{item_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted"

    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 404


def test_item_not_found():
    response = client.get("/api/items/999999")

    assert response.status_code == 404