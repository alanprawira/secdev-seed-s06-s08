from fastapi.testclient import TestClient
from app.main import app
import os  

client = TestClient(app, raise_server_exceptions=False)

def test_logging_hide_password():
    # Ensure log file exists with proper UTF-8 encoding
    if not os.path.exists('app.log'):
        with open('app.log', 'w', encoding='utf-8') as f:
            f.write("")  # Create empty log file
    
    # Make request that will trigger an error and logging
    payload = {"username": "usr", "password": "pwd"}
    resp = client.post("/login_w_error", json=payload)
    print(resp.status_code)
    assert resp.status_code == 500

    # Read log file with explicit UTF-8 encoding to prevent decoding issues
    with open('app.log', 'r', encoding='utf-8') as f:
        file_content = f.read()
        print(f"Log content: {file_content}")
        # Verify password is not exposed in logs
        assert "pwd" not in file_content