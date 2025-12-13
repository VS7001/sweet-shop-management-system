from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_purchase_sweet():
    response = client.post(
        "/api/sweets",
        json={
            "name": "Jalebi",
            "category": "Indian",
            "price": 15,
            "quantity": 10
        }
    )

    sweet_id = response.json()["id"]

    purchase_response = client.post(f"/api/sweets/{sweet_id}/purchase")

    assert purchase_response.status_code == 200
    assert purchase_response.json()["quantity"] == 9


def test_restock_sweet():
    response = client.post(
        "/api/sweets",
        json={
            "name": "Rasgulla",
            "category": "Indian",
            "price": 12,
            "quantity": 5
        }
    )

    sweet_id = response.json()["id"]

    restock_response = client.post(f"/api/sweets/{sweet_id}/restock")

    assert restock_response.status_code == 200
    assert restock_response.json()["quantity"] == 6
