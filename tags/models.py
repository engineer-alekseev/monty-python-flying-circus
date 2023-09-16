from pydantic import BaseModel
from users.models import Meta


class TagsOut(BaseModel):
    id : int
    tag: str


class TagsOutList(BaseModel):
    rows : list[TagsOut]
    meta : Meta

class TagsIn(BaseModel):
    tag: str

