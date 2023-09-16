from datetime import datetime
from pydantic import BaseModel, constr

class UserOut(BaseModel):
    id : int
    username: str
    email: str | None
    is_admin: bool | None
    is_moderator: bool | None
    friends: list[int] | None = []
    created_at: datetime

class Meta(BaseModel):
    skip : int | None = 0
    limit : int | None = 0
    count : int | None = 0

class UserOutList(BaseModel):
    rows : list[UserOut]
    meta : Meta

class UserIn(BaseModel):
    username: str
    password: constr(min_length=4, max_length=16)


class UserUpdate(BaseModel):
    is_admin: bool | None
    is_moderator: bool | None

class User(BaseModel):
    id : int
    username: str
    email: str | None
    hashed_password: str
    is_admin: bool | None
    is_moderator: bool | None
    friends: list[int] | None = []
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
