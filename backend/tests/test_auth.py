def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "test_user", "password": "test123"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "test_user"


def test_login_user(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "test_user", "password": "test123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
