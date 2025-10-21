import logging
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from .models import LoginRequest
from .db import query, query_one

# Get the absolute path to ensure the log file is created
current_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(current_dir, 'app.log')

# Ensure the log file exists by creating it if it doesn't
if not os.path.exists(log_path):
    with open(log_path, 'w') as f:
        f.write("")  # Create empty file

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    filename=log_path,  # Use absolute path
    filemode="a",  # Use 'a' (append) instead of 'w' to preserve content
)

logger = logging.getLogger(__name__)

app = FastAPI(title="secdev-seed-s06-s08")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request, msg: str | None = None):
    # XSS: intentionally render message without escaping via template
    return templates.TemplateResponse("index.html", {"request": request, "message": msg or "Hello!"})

@app.get("/echo", response_class=HTMLResponse)
def echo(request: Request, msg: str | None = None):
    return templates.TemplateResponse("index.html", {"request": request, "message": msg or ""})

@app.get("/search")
def search(q: str | None = None):
    # FIXED: SQLi - Use parameterized queries for LIKE search
    if q:
        # ADD INPUT VALIDATION FOR LONG QUERIES
        if len(q) > 20:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, 
                detail="Request string too long"
            )
        
        sql = "SELECT id, name, description FROM items WHERE name LIKE ?"
        items = query(sql, (f"%{q}%",))
    else:
        sql = "SELECT id, name, description FROM items LIMIT 10"
        items = query(sql)
    return JSONResponse(content={"items": items})

@app.post("/login")
def login(payload: LoginRequest):
    # FIXED: SQLi - Use parameterized queries to prevent SQL injection
    sql = "SELECT id, username FROM users WHERE username = ? AND password = ?"
    row = query_one(sql, (payload.username, payload.password))
    if not row:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # dummy token
    return {"status": "ok", "user": row["username"], "token": "dummy"}

# ADD REQUIRED ENDPOINTS FOR TESTS

@app.get("/error")
def error(request: Request):
    logger.error("Test error endpoint called")
    raise Exception("Test exception for error handling")

@app.get("/test_httpexception")
def test_httpexception():
    raise HTTPException(status_code=400, detail="Test HTTP exception")

@app.post("/login_w_error")
def login_w_error(payload: LoginRequest):
    # Log the request (password will be masked by exception handler)
    logger.info("Login with error endpoint called")
    raise Exception(payload.model_dump())

# Add exception handler to ensure logging works
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )