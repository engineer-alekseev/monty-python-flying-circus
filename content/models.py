from datetime import datetime
from pydantic import BaseModel
from users.models import Meta

class ContentOut(BaseModel):
    id : int
    link_to_storage: str
    is_private: bool
    counter: int
    updated_at: datetime
    created_at: datetime


class ContentOutList(BaseModel):
    rows : list[ContentOut]
    meta : Meta

