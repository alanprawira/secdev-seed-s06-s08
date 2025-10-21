def test_logging_hide_password():
    if not os.path.exists('app.log'):
        with open('app.log', 'w', encoding='utf-8') as f:  # encoding
            f.write("")
    
    payload = {"username": "usr", "password": "pwd"}
    resp = client.post("/login_w_error", json=payload)
    print(resp.status_code)
    assert resp.status_code == 500

    # multiple encodings
    encodings = ['utf-8', 'utf-16', 'latin-1']
    file_content = ""
    
    for encoding in encodings:
        try:
            with open('app.log', 'r', encoding=encoding) as f:
                file_content = f.read()
            break
        except UnicodeDecodeError:
            continue
    
    print(f"Log file content: {file_content}")
    assert "pwd" not in file_content