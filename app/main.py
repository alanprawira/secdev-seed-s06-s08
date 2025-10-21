from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED

from .models import LoginRequest
from .db import query, query_one

app = FastAPI(title="secdev-seed-s06-s08")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request, msg: str | None = None):
    return templates.TemplateResponse("index.html", {"request": request, "message": msg or "Hello!"})

@app.get("/echo", response_class=HTMLResponse)
def echo(request: Request, msg: str | None = None):
    return templates.TemplateResponse("index.html", {"request": request, "message": msg or ""})

@app.get("/search")
def search(q: str | None = None):
    # ✅ CORRECT: Parameterized query for LIKE search
    if q:
        sql = "SELECT id, name, description FROM items WHERE name LIKE ?"
        items = query(sql, (f"%{q}%",))
    else:
        sql = "SELECT id, name, description FROM items LIMIT 10"
        items = query(sql)
    return JSONResponse(content={"items": items})

@app.post("/login")
def login(payload: LoginRequest):
    # ✅ CORRECT: Parameterized query for login
    sql = "SELECT id, username FROM users WHERE username = ? AND password = ?"
    row = query_one(sql, (payload.username, payload.password))
    if not row:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"status": "ok", "user": row["username"], "token": "dummy"}