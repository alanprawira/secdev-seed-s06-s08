from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app, raise_server_exceptions=False)

def test_logging_hide_password():
    # First, ensure app.log exists
    if not os.path.exists('app.log'):
        with open('app.log', 'w') as f:
            f.write("")  # Create empty log file
    
    payload = {"username": "usr", "password": "pwd"}
    resp = client.post("/login_w_error", json=payload)
    print(resp.status_code)
    assert resp.status_code == 500

    # Read the log file we created
    with open('app.log', 'r') as f:
        file_content = f.read()
        print(f"Log file content: {file_content}")
        # Check that password is not visible in plain text
        assert "pwd" not in file_content