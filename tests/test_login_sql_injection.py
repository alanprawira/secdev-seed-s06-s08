from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_should_not_allow_sql_injection():
# We expect that logging in with a username containing an SQL comment should BE denied.
# In the current state of the application, the test will fail (and this is normal until S06).
    payload = {"username": "admin'-- ", "password": "x"}
    resp = client.post("/login", json=payload)
    print(resp.status_code)
    assert resp.status_code == 401, "SQLi-The login bypass must be closed."


def test_login():
    payload = {"username": "admin", "password": "admin"}
    resp = client.post("/login", json=payload)
    print(resp.status_code)
    assert resp.status_code == 200
