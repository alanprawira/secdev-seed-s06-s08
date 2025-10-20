from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_echo_should_escape_script_tags():
    resp = client.get("/echo", params={"msg": "<script>alert(1)</script>"})
# In the protected version, the script should not appear in the response as a tag.
    assert (
        "<script>" not in resp.text
    ), "The output must escape the potential XSS sequence."



def test_echo():
# positive test
    resp = client.get("/echo", params={"msg": "test text"})
    assert (
        "test text" in resp.text
    )
