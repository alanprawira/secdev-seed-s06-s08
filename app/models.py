
from pydantic import BaseModel, StringConstraints
from typing import Annotated

Username = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=3, max_length=48, pattern=r"^[a-zA-Z0-9_.'-]+$")
]

Password = Annotated[
    str,
    StringConstraints(min_length=1, max_length=128)
]


class LoginRequest(BaseModel):
    username: Username
    password: Password

class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
