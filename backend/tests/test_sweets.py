def get_token(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "test_user", "password": "test123"}
    )
    return response.json()["access_token"]


def test_create_sweet(client):
    token = get_token(client)

    response = client.post(
        "/api/v1/sweets/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Rasgulla",
            "category": "Indian",
            "price": 20,
            "quantity": 10
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Rasgulla"


def test_purchase_sweet(client):
    token = get_token(client)

    response = client.post(
        "/api/v1/sweets/1/purchase",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 9
