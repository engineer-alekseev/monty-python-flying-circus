from typing import Optional
from datetime import datetime
from pydantic import BaseModel, constr
from users.models import Meta

    # Column("id", Integer, primary_key=True),
    # Column("link_to_storage", String, nullable=False, unique=True),
    # Column("is_private", Boolean, default=False),
    # Column("counter", Integer, nullable=False, default=1),
    # Column("updated_at", DateTime, nullable=False, default=datetime.now()),
    # Column("created_at", DateTime, nullable=False, default=datetime.now()),

class ContentOut(BaseModel):
    id : int
    username: str
    email: str | None
    is_admin: bool | None
    is_moderator: bool | None
    friends: list[int] | None = []
    created_at: datetime


class ContentOutList(BaseModel):
    rows : list[ContentOut]
    meta : Meta

class ContentIn(BaseModel):
    link_to_storage: str
    is_private: bool | None = False



# class UserUpdate(BaseModel):
#     is_admin: bool | None
#     is_moderator: bool | None

# class User(BaseModel):
#     id : int
#     username: str
#     email: str | None
#     hashed_password: str
#     is_admin: bool | None
#     is_moderator: bool | None
#     friends: list[int] | None = []
#     created_at: datetime

