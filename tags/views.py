from typing import Annotated
from tags.models import TagsIn, TagsOutList
from users.services import get_current_active_user
from users.models import User
from fastapi import Depends
import tags.services as TagsServices

from fastapi import APIRouter


tags_router = APIRouter(prefix='/tags', tags=['tags'])

@tags_router.get("", response_model=TagsOutList)
async def get_public_content(current_user: Annotated[User, Depends(get_current_active_user)],
                        skip: int = 0, limit: int | None = 100,
                        order_by: str = 'id', order_desc: bool = True):
    obj =  await TagsServices.get_tags(skip, limit,
                                        order_by, order_desc)
    return {"rows" : obj, "meta" : {"skip" : skip, "limit" : limit, "count" : len(obj)}}

@tags_router.post("", response_model=TagsIn)
async def post_tag(current_user: Annotated[User, Depends(get_current_active_user)],
                       tag: str):
    return await TagsServices.post_tag(tag)

@tags_router.delete("")
async def delete_content(current_user: Annotated[User, Depends(get_current_active_user)],
                         id: int):
    return await TagsServices.delete_tag(current_user, id)
