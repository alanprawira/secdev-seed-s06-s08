
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_should_positive():
    payload = {"username": "admin", "password": "admin"}
    resp = client.post("/login", json=payload)
    assert resp.status_code == 200, "Неправильные логин и пароль"
