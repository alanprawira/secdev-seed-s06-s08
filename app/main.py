
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import Query
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED

from .models import LoginRequest
from .db import query, query_one, query_one_params, query_params

app = FastAPI(title="secdev-seed-s06-s08")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request, msg: str | None = None):
    # XSS: намеренно рендерим message без экранирования через шаблон (см. index.html)
    return templates.TemplateResponse("index.html", {"request": request, "message": msg or "Hello!"})

@app.get("/echo", response_class=HTMLResponse)
def echo(request: Request, msg: str | None = None):
    return templates.TemplateResponse("index.html", {"request": request, "message": msg or ""})

@app.get("/search")
def search(q: str | None = Query(default=None, min_length=1, max_length=32)):
    # SQLi: намеренно подставляем строку без параметров
    sql = "SELECT id, name, description FROM items WHERE name LIKE ?"
    pattern = f"%{q}%"
    return JSONResponse(content={"items": query_params(sql, (pattern,))})

@app.post("/login")
def login(payload: LoginRequest):
    sql = "SELECT id, username FROM users WHERE username = ? AND password = ?"
    row = query_one_params(sql, (payload.username, payload.password))
    if not row:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # фиктивный токен
    return {"status": "ok", "user": row["username"], "token": "dummy"}
