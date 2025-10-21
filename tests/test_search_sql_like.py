from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_search_should_not_return_all_on_injection():
# For a meaningless request we expect 0, and for an injection we also expect 0 (not all elements)
    resp_noise = client.get("/search", params={"q": "zzzzzzzzz"}).json()
    inj = client.get("/search", params={"q": "' OR '1'='1"}).json()
    assert len(inj["items"]) <= len(
        resp_noise["items"]
    ), "Injecting into LIKE should not result in all elements being returned."


def test_search_long_query():
# For a meaningless request we expect 0, and for an injection we also expect 0 (not all elements)
    resp_long = client.get(
        "/search",
        params={
            "q": "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
        },
    )
    assert resp_long.status_code == 400, "Query too long"


def test_search_query():
    # позитивный тест
    resp_long = client.get(
        "/search",
        params={
            "q": "apple"
        },
    )
    assert resp_long.status_code == 200