from typing import Annotated
from content.models import ContentOut, ContentOutList, ContentIn
from users.services import get_current_active_user
from users.models import User
from fastapi import Depends
import content.services as ContentServices

from fastapi import APIRouter


content_router = APIRouter(prefix='/content', tags=['content'])

@content_router.get("/public")
async def get_public_content(
                        skip: int = 0, limit: int | None = 5,
                        order_by: str = 'created_at', order_desc: bool = True,
                        filter_tag: str | None = None):
    obj =  await ContentServices.get_content(skip, limit,
                                             order_by, order_desc, filter_tag)
    return {"rows" : obj, "meta" : {"skip" : skip, "limit" : limit, "count" : len(obj)}}

@content_router.get("/own", response_model=ContentOutList)
async def get_own_content(current_user: Annotated[User, Depends(get_current_active_user)],
                        skip: int = 0, limit: int | None = 5,
                        order_by: str = 'created_at', order_desc: bool = True,
                        filter_tag: str | None = None):
    obj =  await ContentServices.get_own_content(current_user, skip, limit,
                                             order_by, order_desc, filter_tag)
    return {"rows" : obj, "meta" : {"skip" : skip, "limit" : limit, "count" : len(obj)}}


@content_router.post("", response_model=ContentOut)
async def post_content(current_user: Annotated[User, Depends(get_current_active_user)],
                       content: ContentIn, tag: str | None = None):
    return await ContentServices.post_content(current_user, content, tag)

@content_router.delete("")
async def delete_content(current_user: Annotated[User, Depends(get_current_active_user)],
                         id: int):
    return await ContentServices.delete_content(current_user, id)
