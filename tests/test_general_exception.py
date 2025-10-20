from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_error_query():
# positive test
# check that all Exceptions (!= HTTPException) will be handled by a single handler
    resp_long = client.get("/error")
    assert resp_long.status_code == 500


def test_http_exception_passthrough():
"""
Negative test: check that the HTTPException isn't caught by the shared handler,
If your endpoint uses a different path or code, replace it here.
"""
    resp = client.get("/test_httpexception")
    assert resp.status_code != 500
