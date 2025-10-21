import logging
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from markupsafe import Markup  # ADD THIS

from .models import LoginRequest
from .db import query, query_one


@app.get("/echo", response_class=HTMLResponse)
def echo(request: Request, msg: str | None = None):
    # FIX: Escape user input to prevent XSS
    safe_msg = Markup.escape(msg) if msg else ""
    return templates.TemplateResponse("index.html", {"request": request, "message": safe_msg})

@app.get("/search")
def search(q: str | None = None):
    if q:
        if len(q) > 20 or "'" in q or "\"" in q or ";" in q:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, 
                detail="Invalid search query"
            )
        
        sql = "SELECT id, name, description FROM items WHERE name LIKE ? LIMIT 10"
        items = query(sql, (f"%{q}%",))
    else:
        sql = "SELECT id, name, description FROM items LIMIT 10"
        items = query(sql)
    return JSONResponse(content={"items": items})

@app.post("/login")
def login(payload: LoginRequest):
    if not payload.username or not payload.password:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Username and password required")
    
    if "'" in payload.username or "\"" in payload.username or ";" in payload.username:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid username")
    
    # FIXED: SQLi - Use parameterized queries
    sql = "SELECT id, username FROM users WHERE username = ? AND password = ?"
    row = query_one(sql, (payload.username, payload.password))
    if not row:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return {"status": "ok", "user": row["username"], "token": "dummy"}