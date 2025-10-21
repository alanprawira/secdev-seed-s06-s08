import logging
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from markupsafe import Markup  

from .models import LoginRequest
from .db import query, query_one


current_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(current_dir, 'app.log')

if not os.path.exists(log_path):
    with open(log_path, 'w') as f:
        f.write("")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    filename=log_path,
    filemode="a",
)

logger = logging.getLogger(__name__)

app = FastAPI(title="secdev-seed-s06-s08")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request, msg: str | None = None):
    return templates.TemplateResponse("index.html", {"request": request, "message": msg or "Hello!"})

@app.get("/echo", response_class=HTMLResponse)
def echo(request: Request, msg: str | None = None):
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
    if "'" in payload.username or "\"" in payload.username or ";" in payload.username:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid username")
    
    sql = "SELECT id, username FROM users WHERE username = ? AND password = ?"
    row = query_one(sql, (payload.username, payload.password))
    if not row:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"status": "ok", "user": row["username"], "token": "dummy"}


@app.get("/error")
def error(request: Request):
    logger.error("Test error endpoint called")
    raise Exception("Test exception for error handling")

@app.get("/test_httpexception")
def test_httpexception():
    raise HTTPException(status_code=400, detail="Test HTTP exception")

@app.post("/login_w_error")
def login_w_error(payload: LoginRequest):
    logger.info("Login with error endpoint called")
    raise Exception(payload.model_dump())

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )