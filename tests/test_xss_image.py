from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_echo_should_escape_img_onerror():
    resp = client.get("/echo", params={"msg": '<img src=x onerror=alert("pwn")>'})
    # Тег <img> с onerror не должен попадать в HTML как выполняемый элемент.
    assert "<img>" not in resp.text and "<onerror>" not in resp.text, "Нельзя рендерить теги/атрибуты, которые могут выполнить JS"