def test_logging_hide_password():

    import os
    if os.path.exists('app.log'):
        os.remove('app.log')
    
    payload = {"username": "usr", "password": "pwd"}
    resp = client.post("/login_w_error", json=payload)
    print(resp.status_code)
    assert resp.status_code == 500

    with open('app.log', 'r') as f:
        file = f.read()