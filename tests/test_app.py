from app import app


def test_home_page_loads():
    client = app.test_client()
    assert client.get("/").status_code == 200


def test_form_check_shows_result():
    client = app.test_client()
    resp = client.post("/", data={"password": "123456"})
    assert b"Weak" in resp.data


def test_api_check():
    client = app.test_client()
    resp = client.post("/api/check", json={"password": "T7#kLp9!vQ2zRm4$"})
    assert resp.get_json()["level"] == "Strong"


def test_health():
    assert app.test_client().get("/health").get_json() == {"status": "ok"}
