from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_search_sweets_by_name():
    client.post(
        "/api/sweets",
        json={
            "name": "Barfi",
            "category": "Indian",
            "price": 20,
            "quantity": 50
        }
    )

    response = client.get("/api/sweets/search?name=Barfi")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Barfi"

def test_search_sweets_by_category():
    client.post(
        "/api/sweets",
        json={
            "name": "Rasgulla",
            "category": "Bengali",
            "price": 25,
            "quantity": 10
        }
    )

    response = client.get("/api/sweets/search?category=Bengali")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_search_sweets_by_price_range():
    client.post(
        "/api/sweets",
        json={
            "name": "Peda",
            "category": "Indian",
            "price": 40,
            "quantity": 5
        }
    )

    response = client.get("/api/sweets/search?min_price=30&max_price=50")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_update_sweet():
    create_response = client.post(
        "/api/sweets",
        json={
            "name": "Halwa",
            "category": "Indian",
            "price": 30,
            "quantity": 10
        }
    )

    sweet_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/sweets/{sweet_id}",
        json={
            "name": "Gajar Halwa",
            "category": "Indian",
            "price": 35,
            "quantity": 8
        }
    )

    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Gajar Halwa"
    assert update_response.json()["price"] == 35


def test_delete_sweet():
    create_response = client.post(
        "/api/sweets",
        json={
            "name": "Kaju Katli",
            "category": "Indian",
            "price": 50,
            "quantity": 5
        }
    )

    sweet_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/sweets/{sweet_id}")
    assert delete_response.status_code == 204

    get_response = client.get("/api/sweets")
    assert all(s["id"] != sweet_id for s in get_response.json())
