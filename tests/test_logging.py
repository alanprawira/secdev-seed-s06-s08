from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app, raise_server_exceptions=False)

def test_logging_hide_password():
    # PASTIKAN file log ada (seperti di test yang berhasil)
    if not os.path.exists('app.log'):
        with open('app.log', 'w') as f:
            f.write("")  # Create empty log file
    
    payload = {"username": "usr", "password": "pwd"}
    resp = client.post("/login_w_error", json=payload)
    print(resp.status_code)
    assert resp.status_code == 500

    with open('app.log', 'r') as f:
        file = f.read()
        print(f"Log content: {file}")  # Debug print
        assert "pwd" not in file