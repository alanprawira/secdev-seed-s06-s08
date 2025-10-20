from pydantic import BaseModel


class LoginRequest(BaseModel):
# Simplified, without length/format restrictions for S06
    username: str
    password: str


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
