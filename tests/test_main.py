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
    response = client.get("/api/items/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"


def test_update_item():
    response = client.put(
        "/api/items/1",
        json={"name": "Gaming Laptop", "price": 1500.0}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Gaming Laptop"


def test_delete_item():
    response = client.delete("/api/items/2")

    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted"


def test_item_not_found():
    response = client.get("/api/items/999")

    assert response.status_code == 404