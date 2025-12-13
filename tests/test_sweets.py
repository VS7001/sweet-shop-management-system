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
