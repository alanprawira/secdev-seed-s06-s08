
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_long_parameter():
    search_param = "z" * 40
    resp_noise = client.get("/search", params={"q": search_param})
    assert resp_noise.status_code == 422 , "Длина q должна быть ограничена"
